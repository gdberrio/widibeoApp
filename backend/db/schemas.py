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


# Base model for Stream
class StreamBase(BaseModel):
    connection_id: str
    name: str
    cursor_field_defined_by_source: bool


# Models for Stream creation and read
class StreamCreate(StreamBase):
    pass


class Stream(StreamBase):
    id: int

    class Config:
        orm_mode = True


# Base model for StreamProperty
class StreamPropertyBase(BaseModel):
    field: str
    stream_id: int


# Models for StreamProperty creation and read
class StreamPropertyCreate(StreamPropertyBase):
    pass


class StreamProperty(StreamPropertyBase):
    id: int

    class Config:
        orm_mode = True


# Base model for StreamSyncMode
class StreamSyncModeBase(BaseModel):
    mode: str
    stream_id: int


# Models for StreamSyncMode creation and read
class StreamSyncModeCreate(StreamSyncModeBase):
    pass


class StreamSyncMode(StreamSyncModeBase):
    id: int

    class Config:
        orm_mode = True


# Base model for StreamPrimaryKey
class StreamPrimaryKeyBase(BaseModel):
    field: str
    stream_id: int


# Models for StreamPrimaryKey creation and read
class StreamPrimaryKeyCreate(StreamPrimaryKeyBase):
    pass


class StreamPrimaryKey(StreamPrimaryKeyBase):
    id: int

    class Config:
        orm_mode = True


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
