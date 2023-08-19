from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from airbyte_service import (
    AirbyteAuthService,
    get_google_ads_consent_url,
    create_google_ads_source,
    create_azure_destination,
    create_connection,
)
from dotenv import load_dotenv
import os

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")
azure_account_name = os.getenv("azure_account_name")
azure_storage_key = os.getenv("azure_account_storage_key")
azure_test_destination_id = os.getenv("azure_test_destination_id")
gads_test_source_id = os.getenv("gads_test_source_id")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/googleads_oauth")
async def googleads_oauth():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    consent_url = get_google_ads_consent_url(
        airbyte_auth=airbyte_auth, workspace_id=testing_workspace_id
    )
    return RedirectResponse(consent_url)


@app.get("/oauth_callback")
async def callback(secret_id: str):
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_google_ads_source(
        airbyte_auth=airbyte_auth,
        workspace_id=testing_workspace_id,
        secret_id=secret_id,
    )
    return {"response": response}


@app.get("/azure_destination")
async def azure_destination():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_azure_destination(
        airbyte_auth=airbyte_auth,
        workspace_id=testing_workspace_id,
        azure_blob_storage_account_name=azure_account_name,
        azure_blob_storage_account_key=azure_storage_key,
    )
    return {"response": response}


@app.get("/create_connection")
async def create_gads_connection():
    airbyte_auth = AirbyteAuthService(airbyte_token=airbyte_key)
    response = create_connection(
        airbyte_auth=airbyte_auth,
        source_id=gads_test_source_id,
        destination_id=azure_test_destination_id,
    )

    return {"response": response}
