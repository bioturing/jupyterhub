from typing import Optional
from sqlalchemy.orm import Session
import logging

from datetime import datetime
import app.models.version as models
import app.schemas.tool as schemas

logger = logging.getLogger("gunicorn.error")
def get_notebook_versions(db: Session, nb_uuid: str, offset: Optional[int], limit: Optional[int]):
    return db.query(models.NotebookVersion).filter(models.NotebookVersion.notebook_uuid == nb_uuid).offset(offset).limit(limit).all()

def get_notebook_version(db: Session, nb_uuid: str, version: str):
    db_version = db.query(models.NotebookVersion).filter( \
                models.NotebookVersion.notebook_uuid == nb_uuid \
                and models.NotebookVersion.name == version).first()
    return db_version

def create_notebook_version(db: Session, nb_version: schemas.NBVersionCreate):
    db_nbversion = models.NotebookVersion(**nb_version.dict())
    db_nbversion.time_added = datetime.now()
    db.add(db_nbversion)
    db.commit()
    db.refresh(db_nbversion)
    return db_nbversion
