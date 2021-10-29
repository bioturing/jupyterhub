from typing import Optional
from sqlalchemy.orm import Session
import logging

from datetime import datetime
import app.models.notebook as models
import app.schemas.notebook as schemas

def get_notebook(db: Session, nb_uuid: str):
    return db.query(models.NotebookRecord).filter(models.NotebookRecord.uuid == nb_uuid).first()

def get_all_notebooks(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookRecord).offset(offset).limit(limit).all() 

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


