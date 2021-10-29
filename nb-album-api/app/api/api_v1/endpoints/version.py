from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional, List

import app.crud.category as crud
from app.api.deps import get_session
from app.schemas.version import NBVersionCreate, NBVersionRead

router = APIRouter()

@router.post("/", response_model=NBVersionRead)
def create_notebook_version(*, session: Session = Depends(get_session), nbversion: NBVersionCreate):
    db_notebook = crud.get_notebook(session, nbversion.notebook_uuid)
    if not db_notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    db_nbversion_maybe = crud.get_notebook_version(session, nbversion.notebook_uuid, nbversion.name)
    if db_nbversion_maybe:
        raise HTTPException(status_code=400, detail="Version already existed")
    db_nbversion = crud.create_notebook_version(session, nbversion)
    return db_nbversion

@router.get("/{notebook_uuid}", response_model=List[NBVersionRead])
def get_notebook_versions(
        *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    notebook_uuid: str
):
    db_notebook = crud.get_notebook(session, notebook_uuid)
    if not db_notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    versions = crud.get_notebook_versions(session, notebook_uuid, offset, limit)
    return versions

@router.delete("/{notebook_uuid}/{version_id}")
def delete_version(*, session: Session = Depends(get_session), notebook_uuid: str, version: str):
    db_notebook = crud.get_notebook(session, notebook_uuid)
    if not db_notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    db_version = crud.get_notebook_version(session, notebook_uuid, version)
    if not db_version:
        raise HTTPException(status_code=404, detail="Notebook Version not found")
    session.delete(db_version)
    session.commit()
    return {"ok": True}