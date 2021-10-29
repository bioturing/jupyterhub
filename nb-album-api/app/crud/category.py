from typing import Optional
from sqlalchemy.orm import Session
import logging

from datetime import datetime
import app.models.category as models
import app.schemas.category as schemas

def get_all_categories(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookCategory).offset(offset).limit(limit).all()

def get_category_byname(db: Session, category: str):
    return db.query(models.NotebookCategory).filter(models.NotebookCategory.name == category).first()

def get_category_byid(db: Session, id: int):
    return db.get(models.NotebookCategory, id)

def create_category_byname(db: Session, name: str, des: str = ""):
    db_cat = models.NotebookCategory(name=name.lower(), description=des)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    logger.debug("Created the new category")
    return db_cat


