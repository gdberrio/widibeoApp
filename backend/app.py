from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from airbyte_service import AirbyteAuthService, get_google_ads_consent_url
from dotenv import load_dotenv
import os

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")

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
    return {"secret_id": secret_id}
