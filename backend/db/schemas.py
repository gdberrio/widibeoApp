from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class WorkspaceBase(BaseModel):
    user_id: int


class WorkspaceCreate(WorkspaceBase):
    pass


class Workspace(WorkspaceBase):
    id: int

    class Config:
        orm_mode = True


class DestinationBase(BaseModel):
    workspace_id: int


class DestinationCreate(DestinationBase):
    pass


class Destination(DestinationBase):
    id: int

    class Config:
        orm_mode = True


class SourceBase(BaseModel):
    workspace_id: int


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    id: int

    class Config:
        orm_mode = True


class ConnectionBase(BaseModel):
    source_id: int
    destination_id: int


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    id: int

    class Config:
        orm_mode = True


class StreamPropertyBase(BaseModel):
    connection_id: int
    key: str
    value: str


class StreamPropertyCreate(StreamPropertyBase):
    pass


class StreamProperty(StreamPropertyBase):
    id: int

    class Config:
        orm_mode = True
