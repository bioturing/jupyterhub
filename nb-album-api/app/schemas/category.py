from typing import List, Optional, Any
from pydantic import BaseModel

from app.models.category import NotebookCategory
from .notebook import NotebookRead

class NBCategoryBase(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    notebook_count: Optional[int]

    @classmethod
    def from_orm_(cls, orm: NotebookCategory):
        cat_model = cls.from_orm(orm)
        cat_model.notebook_count = len(orm.notebooks)
        return cat_model

    class Config:
        orm_mode = True

class NBCategoryCreate(BaseModel):
    name: str
    description: Optional[str]

class NBCategoryRead(NBCategoryBase):
    notebooks: List[Any] = []

    @classmethod
    def from_orm_(cls, orm: NotebookCategory):
        cat_model = cls.from_orm(orm)
        cat_model.notebooks = [NotebookRead.from_orm_(ass.notebook) for ass in orm.notebooks]
        return cat_model

    class Config:
        orm_mode = True
