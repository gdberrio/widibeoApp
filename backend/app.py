from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from airbyte_service.base_functions import (
    AirbyteAuthService,
    get_google_ads_consent_url,
    create_google_ads_source,
    create_s3_destination,
    create_connection,
    get_stream_properties,
)
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db import models, schemas, crud

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")
source_id = os.getenv("gads_test_source_id")
aws_access_key = os.getenv("aws_access_key")
aws_access_secret = os.getenv("aws_access_secret")
destination_id = os.getenv("s3_destination_id")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/workspace/", response_model=schemas.Workspace)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = crud.get_workspace(db, workspace_id=workspace.id)
    if db_workspace:
        raise HTTPException(status_code=400, detail="Workspace already registered")
    return crud.create_workspace(db=db, workspace=workspace)


@app.get("/googleads_oauth")
async def googleads_oauth():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    if testing_workspace_id is None:
        raise HTTPException(status_code=400, detail="No workspace_id")
    consent_url = get_google_ads_consent_url(
        airbyte_auth=airbyte_auth, workspace_id=testing_workspace_id
    )
    if consent_url is None:
        raise HTTPException(status_code=400, detail="No consent URL returned")
    return RedirectResponse(consent_url)


@app.get("/oauth_callback", response_model=schemas.Source)
async def callback(secret_id: str, db: Session = Depends(get_db)):
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


@app.get("/s3_destination", response_model=schemas.Destination)
async def s3_destination(db: Session = Depends(get_db)):
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    if testing_workspace_id is None:
        raise HTTPException(status_code=400, detail="No workspace_id")
    if aws_access_key is None:
        raise HTTPException(status_code=400, detail="No aws_access_key")
    if aws_access_secret is None:
        raise HTTPException(status_code=400, detail="No aws_access_secret")
    response = create_s3_destination(
        airbyte_auth=airbyte_auth,
        workspace_id=testing_workspace_id,
        aws_access_key=aws_access_key,
        aws_access_secret=aws_access_secret,
        s3_bucket_name="widibeodatalake",
        s3_bucket_path="airbyte",
    )

    if response is None:
        raise HTTPException(status_code=400, detail="response is None")

    if response.destination_response is None:
        raise HTTPException(status_code=400, detail="response is None")

    destination_id = response.destination_response.destination_id
    destination = schemas.DestinationCreate(
        workspace_id=testing_workspace_id, id=destination_id
    )

    db_destination = crud.get_destination(db, destination_id=destination_id)
    if db_destination:
        raise HTTPException(status_code=400, detail="Destination already registered")
    return crud.create_destination(db, destination)


@app.get("/create_connection")
async def create_gads_connection():
    if source_id is None:
        return {"response": "source_id"}
    if destination_id is None:
        return {"response": "destination_id"}

    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_connection(
        airbyte_auth=airbyte_auth,
        source_id=source_id,
        destination_id=destination_id,
    )

    return {"response": response}


@app.get("/stream_properties")
async def stream_properties():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = get_stream_properties(
        airbyte_auth=airbyte_auth,
        source_id="539bc4c5-dad0-49a2-928b-85025b4c0498",
        destination_id="967deeca-2fa4-4e87-8711-e116519420f9",
    )

    return {"response": response}
