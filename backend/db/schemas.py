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
    workspace_id: int
    id: str


class DestinationCreate(DestinationBase):
    pass


class Destination(DestinationBase):
    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    workspace_id: int
    id: str


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    class Config:
        from_attributes = True


class ConnectionBase(BaseModel):
    source_id: int
    destination_id: int
    id: str


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    class Config:
        from_attributes = True


class StreamPropertyBase(BaseModel):
    connection_id: int
    key: str
    value: str
    id: str


class StreamPropertyCreate(StreamPropertyBase):
    pass


class StreamProperty(StreamPropertyBase):
    class Config:
        from_attributes = True
