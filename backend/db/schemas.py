from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class WorkspaceBase(BaseModel):
    user_id: int
    id: str


class WorkspaceCreate(WorkspaceBase):
    pass


class Workspace(WorkspaceBase):
    class Config:
        from_attributes = True


class DestinationBase(BaseModel):
    workspace_id: str
    id: str


class DestinationCreate(DestinationBase):
    pass


class Destination(DestinationBase):
    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    workspace_id: str
    id: str


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    class Config:
        from_attributes = True


class ConnectionBase(BaseModel):
    source_id: str
    destination_id: str
    id: str


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    class Config:
        from_attributes = True


class StreamPropertyBase(BaseModel):
    connection_id: str
    key: str
    value: str
    id: str


class StreamPropertyCreate(StreamPropertyBase):
    pass


class StreamProperty(StreamPropertyBase):
    class Config:
        from_attributes = True


class S3DestinationRequest(BaseModel):
    workspace_id: str
    aws_access_key: str
    aws_access_secret: str
    s3_bucket_name: str = "widibeodatalake"  # Default value if you want
    s3_bucket_path: str = "airbyte"  # Default value if you want


class WorkspaceRequest(BaseModel):
    workspace_id: str


class ConnectionRequest(BaseModel):
    source_id: str
    destination_id: str
