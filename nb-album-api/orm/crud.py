from typing import Optional
from sqlalchemy.orm import Session
import logging

from datetime import datetime
from . import models, schemas

logger = logging.getLogger("gunicorn.error")

def get_notebook(db: Session, nb_uuid: str):
    return db.query(models.NotebookRecord).filter(models.NotebookRecord.uuid == nb_uuid).first()

def get_all_notebooks(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookRecord).offset(offset).limit(limit).all() 

def get_all_categories(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookCategory).offset(offset).limit(limit).all()

def get_all_tools(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookTool).offset(offset).limit(limit).all()

def get_category_byname(db: Session, category: str):
    return db.query(models.NotebookCategory).filter(models.NotebookCategory.name == category).first()

def get_category_byid(db: Session, id: int):
    return db.get(models.NotebookCategory, id)

def get_tool_byid(db: Session, id: int):
    return db.get(models.NotebookTool, id)

def get_tool_byname(db: Session, tool: str):
    return db.query(models.NotebookTool).filter(models.NotebookTool.name == tool).first()

def get_notebook_versions(db: Session, nb_uuid: str, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookVersion).filter(models.NotebookVersion.notebook_uuid == nb_uuid).offset(offset).limit(limit).all()

def get_notebook_version(db: Session, nb_uuid: str, version: str):
    db_version = db.query(models.NotebookVersion).filter( \
                models.NotebookVersion.notebook_uuid == nb_uuid \
                and models.NotebookVersion.name == version).first()
    return db_version

def create_category_byname(db: Session, name: str, des: str = ""):
    db_cat = models.NotebookCategory(name=name.lower(), description=des)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    logger.debug("Created the new category")
    return db_cat

def create_tool_byname(db: Session, name: str):
    db_tool = models.NotebookTool(name=name)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def create_tool(db: Session, tool:schemas.NBToolCreate):
    """ Create new NotebookTool record
    """
    kwargs = tool.dict()
    db_tool = models.NotebookTool(**kwargs)
    db.add(db_tool) 
    db.commit()
    db.refresh(db_tool)
    return db_tool

def create_notebook(db: Session, notebook: schemas.NotebookCreate):
    """ Create new NotebookRecord. Add the categories and tools by name if not exists
    """
    kwargs = notebook.dict()
    add_categories = kwargs["add_categories"]
    add_tools = kwargs["add_tools"]

    kwargs.pop("add_categories", None)
    kwargs.pop("add_tools", None)

    db_notebook = models.NotebookRecord(**kwargs)
    db_notebook.time_added = datetime.now()
    db_notebook.time_modified = datetime.now()
    
    for cat in add_categories:
        db_cat_maybe = get_category_byname(db, cat)
        if not db_cat_maybe:
            logger.debug("Gonna created the new category")
            db_cat = create_category_byname(db, cat)
            db_notebook.categories.append(models.NotebookCategoryAssociation(category = db_cat))
        else:
            db_notebook.categories.append(models.NotebookCategoryAssociation(category = db_cat_maybe))

    db.add(db_notebook) 
    db.commit()
    db.refresh(db_notebook)

    for tool in add_tools:
        db_tool_maybe = get_tool_byname(db, tool)
        if not db_tool_maybe:
            db_tool = create_tool_byname(db, tool)
            db_notebook.tools.append(models.NotebookToolAssociation(tool = db_tool))
        else:
            db_notebook.tools.append(models.NotebookToolAssociation(tool = db_tool_maybe))

    db.add(db_notebook) 
    db.commit()
    db.refresh(db_notebook)

    return db_notebook

def create_notebook_version(db: Session, nb_version: schemas.NBVersionCreate):
    db_nbversion = models.NotebookVersion(**nb_version.dict())
    db_nbversion.time_added = datetime.now()
    db.add(db_nbversion)
    db.commit()
    db.refresh(db_nbversion)
    return db_nbversion