from typing import List, Any
from pydantic import BaseModel

from app.models.notebook import NotebookRecord

class NotebookBase(BaseModel):
    uuid: str
    name: str
    maintainer: str
    source: str
    description: str
    format: str

class NotebookCreate(NotebookBase):
    add_categories: List[str] = []
    add_tools: List[str] = []

class NotebookRead(NotebookBase):
    categories: List[Any] = []
    versions: List[Any] = []
    tools: List[Any] = []

    @classmethod
    def from_orm_(cls, orm: NotebookRecord):
        nb_schem = cls.from_orm(orm)
        nb_schem.categories = [ass.category.name for ass in orm.categories]
        nb_schem.tools = [ass.tool.name for ass in orm.tools]
        nb_schem.versions = [ver.name for ver in orm.versions]
        return nb_schem
    
    class Config:
        orm_mode = True