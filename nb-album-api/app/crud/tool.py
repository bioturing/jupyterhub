from typing import Optional
from sqlalchemy.orm import Session
import logging

from datetime import datetime
from . import models, schemas
import app.models.tool as models
import app.schemas.tool as schemas


def get_all_tools(db: Session, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookTool).offset(offset).limit(limit).all()

def get_tool_byid(db: Session, id: int):
    return db.get(models.NotebookTool, id)

def get_tool_byname(db: Session, tool: str):
    return db.query(models.NotebookTool).filter(models.NotebookTool.name == tool).first()

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


