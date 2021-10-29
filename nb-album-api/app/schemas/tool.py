from typing import List, Optional, Any
from pydantic import BaseModel

from app.models.tool import NotebookTool
from .notebook import NotebookRead

class NBToolBase(BaseModel):
    id: Optional[int]
    name: str
    notebook_count: Optional[int]

    @classmethod
    def from_orm_(cls, orm: NotebookTool):
        cat_model = cls.from_orm(orm)
        cat_model.notebook_count = len(orm.notebooks)
        return cat_model

    class Config:
        orm_mode = True

class NBToolCreate(BaseModel):
    name: str
    description: Optional[str]
    homepage: Optional[str]
    pass

class NBToolRead(BaseModel):
    name: str
    notebooks: List[Any] = []

    @classmethod
    def from_orm_(cls, orm: NotebookTool):
        tool_model = cls.from_orm(orm)
        tool_model.notebooks = [NotebookRead.from_orm_(ass.notebook) for ass in orm.notebooks]
        return tool_model

    class Config:
        orm_mode = True