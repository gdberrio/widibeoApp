from sqlalchemy.orm import Session
from db import models, schemas


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Workspace CRUD operations
def get_workspace(db: Session, workspace_id: str):
    return (
        db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()
    )


def create_workspace(db: Session, workspace: schemas.WorkspaceCreate):
    db_workspace = models.Workspace(**workspace.model_dump())
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


# Destination CRUD operations
def get_destination(db: Session, destination_id: str):
    return (
        db.query(models.Destination)
        .filter(models.Destination.id == destination_id)
        .first()
    )


def create_destination(db: Session, destination: schemas.DestinationCreate):
    db_destination = models.Destination(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination


# Source CRUD operations
def get_source(db: Session, source_id: str):
    return db.query(models.Source).filter(models.Source.id == source_id).first()


def create_source(db: Session, source: schemas.SourceCreate):
    db_source = models.Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


# Connection CRUD operations
def get_connection(db: Session, connection_id: str):
    return (
        db.query(models.Connection)
        .filter(models.Connection.id == connection_id)
        .first()
    )


def create_connection(db: Session, connection: schemas.ConnectionCreate):
    db_connection = models.Connection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


# StreamProperty CRUD operations
def get_stream_property(db: Session, stream_property_id: str):
    return (
        db.query(models.StreamProperty)
        .filter(models.StreamProperty.id == stream_property_id)
        .first()
    )


def insert_stream_data(db: Session, source_id: str, destination_id: str, data: list):
    for item in data:
        # Insert Stream
        print("STREAM: addiding stream")
        stream = models.Stream(
            name=item["streamName"],
            cursor_field_defined_by_source=item["sourceDefinedCursorField"],
            source_id=source_id,
            destination_id=destination_id,
        )
        db.add(stream)
        db.commit()

        print("STREAM: addiding property")
        # Insert StreamProperty
        for prop in item.get("propertyFields", []):
            db.add(models.StreamProperty(field=prop[0], stream_id=stream.id))
            db.commit()

        print("STREAM: addiding syncModes")
        # Insert StreamSyncMode
        for mode in item.get("syncModes", []):
            db.add(models.StreamSyncMode(mode=mode, stream_id=stream.id))
            db.commit()

        print("STREAM: addiding StreamPrimaryKey")
        # Insert StreamPrimaryKey
        for key in item.get("sourceDefinedPrimaryKey", []):
            db.add(models.StreamPrimaryKey(field=key[0], stream_id=stream.id))
            db.commit()
