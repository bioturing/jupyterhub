from datetime import datetime
from datetime import time

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, create_engine

from setting import NB_DB_DIR

class NotebookCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

class NotebookRecordBase(SQLModel):
    uuid: str 
    name: str 
    maintainer: str
    source: str
    download_link: str
    version: str
    default_route: str
    sha256: str
    description: str
    category_id: int = Field(foreign_key="notebookcategory.id")
    format: str
    tools: str
    token: Optional[str] = Field(default=None)
    category: NotebookCategory = Relationship(sa_relationship_kwargs={'foreign_keys':[category_id]})

class NotebookRecord(NotebookRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_added: Optional[str]

class NotebookRecordCreate(NotebookRecordBase):
    pass

class NotebookRecordRead(NotebookRecordBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_added: Optional[str]
    token: None

sqlite_file_name = f"{NB_DB_DIR}/notebook-album.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"