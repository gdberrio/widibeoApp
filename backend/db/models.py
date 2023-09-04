from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    workspace = relationship("Workspace", uselist=False, back_populates="user")


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="workspace")
    destinations = relationship("Destination", back_populates="workspace")
    sources = relationship("Source", back_populates="workspace")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))

    workspace = relationship("Workspace", back_populates="destinations")
    connections = relationship("Connection", back_populates="destination")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))

    workspace = relationship("Workspace", back_populates="sources")
    connections = relationship("Connection", back_populates="source")


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    source = relationship("Source", back_populates="connections")
    destination = relationship("Destination", back_populates="connections")
    properties = relationship("StreamProperty", back_populates="connection")


class StreamProperty(Base):
    __tablename__ = "stream_properties"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("connections.id"))
    key = Column(String, index=True)
    value = Column(String)

    connection = relationship("Connection", back_populates="properties")
