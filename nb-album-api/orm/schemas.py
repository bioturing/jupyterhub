from typing import List, Optional, Any, Set
from pydantic import BaseModel

from .models import NotebookRecord, NotebookVersion, NotebookCategory, NotebookTool

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

class NBVersionBase(BaseModel):
    name: str

class NBVersionRead(NBVersionBase):
    sha256: str
    download_link: str
    default_route: str
    token: str

    class Config:
        orm_mode = True

class NBVersionCreate(NBVersionBase):
    sha256: str
    download_link: str
    default_route: str
    token: str
    notebook_uuid: str

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