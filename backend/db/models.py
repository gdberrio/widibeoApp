from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    workspace = relationship("Workspace", uselist=False, back_populates="user")


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="workspace")
    destinations = relationship("Destination", back_populates="workspace")
    sources = relationship("Source", back_populates="workspace")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(String, primary_key=True, index=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"))

    workspace = relationship("Workspace", back_populates="destinations")
    connections = relationship("Connection", back_populates="destination")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, index=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"))

    workspace = relationship("Workspace", back_populates="sources")
    connections = relationship("Connection", back_populates="source")


class Connection(Base):
    __tablename__ = "connections"

    id = Column(String, primary_key=True, index=True)
    source_id = Column(String, ForeignKey("sources.id"))
    destination_id = Column(String, ForeignKey("destinations.id"))

    source = relationship("Source", back_populates="connections")
    destination = relationship("Destination", back_populates="connections")
    streams = relationship("Stream", back_populates="connection")


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(String, ForeignKey("connections.id"), nullable=True)
    name = Column(String)
    source_id = Column(String, ForeignKey("sources.id"))
    destination_id = Column(String, ForeignKey("destinations.id"))
    cursor_field_defined_by_source = Column(Boolean)

    sync_modes = relationship("StreamSyncMode", back_populates="stream")
    properties = relationship("StreamProperty", back_populates="stream")
    connection = relationship("Connection", back_populates="streams")
    primary_keys = relationship("StreamPrimaryKey", back_populates="stream")


class StreamProperty(Base):
    __tablename__ = "stream_properties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    field = Column(String, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))

    stream = relationship("Stream", back_populates="properties")


class StreamSyncMode(Base):
    __tablename__ = "stream_sync_modes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mode = Column(String, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))

    stream = relationship("Stream", back_populates="sync_modes")


class StreamPrimaryKey(Base):
    __tablename__ = "stream_primary_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    field = Column(String, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))

    stream = relationship("Stream", back_populates="primary_keys")


class SyncJobs(Base):
    __tablename__ = "sync_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    job_type = Column(String)
