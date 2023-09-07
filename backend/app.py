from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db import models, schemas, crud

from routers import airbyte

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


app.include_router(airbyte.router)


@app.post("/workspace/", response_model=schemas.Workspace)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = crud.get_workspace(db, workspace_id=workspace.id)
    if db_workspace:
        raise HTTPException(status_code=400, detail="Workspace already registered")
    return crud.create_workspace(db=db, workspace=workspace)
