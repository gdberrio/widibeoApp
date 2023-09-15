from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from db.database import engine
from db import models

from routers import airbyte, llm

load_dotenv()
airbyte_key = os.getenv("airbyte_key")
testing_workspace_id = os.getenv("testing_workspace_id")
source_id = os.getenv("gads_test_source_id")
aws_access_key = os.getenv("aws_access_key")
aws_access_secret = os.getenv("aws_access_secret")
destination_id = os.getenv("s3_destination_id")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(airbyte.router)
app.include_router(llm.router)


@app.get("/oauth", response_class=HTMLResponse)
async def oauth(request: Request):
    return templates.TemplateResponse("oauth.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
