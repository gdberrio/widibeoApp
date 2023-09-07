import redis
from fastapi import APIRouter, Depends, Form, Response, HTTPException
from db import schemas, crud
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from airbyte_service.base_functions import (
    AirbyteAuthService,
    get_google_ads_consent_url,
    create_google_ads_source,
    create_s3_destination,
    create_connection,
    get_stream_properties,
)
from db.database import SessionLocal
from dotenv import load_dotenv
import os
from uuid import uuid4

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


r = redis.Redis(host="localhost", port=6379, db=0)

router = APIRouter(prefix="/v1/airbyte")


@router.post("/s3_destination", response_model=schemas.Destination)
async def s3_destination(
    request: schemas.S3DestinationRequest, db: Session = Depends(get_db)
):
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_s3_destination(
        airbyte_auth=airbyte_auth,
        workspace_id=request.workspace_id,
        aws_access_key=request.aws_access_key,
        aws_access_secret=request.aws_access_secret,
        s3_bucket_name=request.s3_bucket_name,
        s3_bucket_path=request.s3_bucket_path,
    )

    if response is None:
        raise HTTPException(status_code=400, detail="response is None")

    if response.destination_response is None:
        raise HTTPException(status_code=400, detail="response is None")

    destination_id = response.destination_response.destination_id
    destination = schemas.DestinationCreate(
        workspace_id=request.workspace_id, id=destination_id
    )

    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination:
        raise HTTPException(status_code=400, detail="Destination already registered")
    return crud.create_destination(db, destination)


@router.post("/googleads_oauth")
async def googleads_oauth(response: Response, workspace_id: str = Form(...)):
    state = str(uuid4())
    r.setex(state, 600, workspace_id)
    response.set_cookie(key="oauth_state", value=state, max_age=600)
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    consent_url = get_google_ads_consent_url(
        airbyte_auth=airbyte_auth, workspace_id=workspace_id
    )
    if consent_url is None:
        raise HTTPException(status_code=400, detail="No consent URL returned")

    return RedirectResponse(consent_url)


@router.get("/oauth_callback", response_model=schemas.Source)
async def callback(secret_id: str, db: Session = Depends(get_db)):
    # TODO: Once you have user management, you need to get the workspace_id from the session_id, not an env var
    if testing_workspace_id is None:
        raise HTTPException(status_code=400, detail="No workspace_id")
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_google_ads_source(
        airbyte_auth=airbyte_auth,
        workspace_id=testing_workspace_id,
        secret_id=secret_id,
    )
    if response is None:
        raise HTTPException(status_code=400, detail="response is None")
    if response.source_response is None:
        raise HTTPException(status_code=400, detail="response is None")

    source_id = response.source_response.source_id

    source = schemas.SourceCreate(workspace_id=testing_workspace_id, id=source_id)
    db_source = crud.get_source(db, source_id=source_id)

    if db_source:
        raise HTTPException(status_code=400, detail="Source already registered")
    return crud.create_source(db, source)


@router.post("/create_connection", response_model=schemas.Connection)
async def create_airbyte_connection(
    request: schemas.ConnectionRequest, db: Session = Depends(get_db)
):
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_connection(
        airbyte_auth=airbyte_auth,
        source_id=request.source_id,
        destination_id=request.destination_id,
    )

    if response is None:
        raise HTTPException(status_code=400, detail="response is None")
    if response.connection_response is None:
        raise HTTPException(status_code=400, detail="response is None")

    connection_id = response.connection_response.connection_id
    connection = schemas.ConnectionCreate(
        source_id=request.source_id,
        destination_id=request.destination_id,
        id=connection_id,
    )
    db_connection = crud.get_connection(db, connection_id=connection_id)
    if db_connection:
        raise HTTPException(status_code=400, detail="Connection already registered")

    return crud.create_connection(db, connection)


@router.post("/stream_properties")
async def stream_properties():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = get_stream_properties(
        airbyte_auth=airbyte_auth,
        source_id="539bc4c5-dad0-49a2-928b-85025b4c0498",
        destination_id="967deeca-2fa4-4e87-8711-e116519420f9",
    )

    return {"response": response}
