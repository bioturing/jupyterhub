from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional, List

import app.crud.notebook as crud
from app.api.deps import get_session
from app.schemas.notebook import NotebookRead, NotebookCreate, NotebookBase

router = APIRouter()

"""
Notebook APIs
"""
@router.post("/", response_model=NotebookRead)
def create_notebook(*, session: Session = Depends(get_session), nb: NotebookCreate):
    db_notebook_maybe = crud.get_notebook(session, nb.uuid)
    if db_notebook_maybe:
        raise HTTPException(status_code=400, detail="Notebook already existed")
    db_notebook = crud.create_notebook(session, nb)
    notebook_model = NotebookRead.from_orm_(db_notebook)
    return notebook_model

@router.get("/", response_model=List[NotebookRead])
def read_notebooks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    notebooks = crud.get_all_notebooks(session, offset, limit) 
    notebook_models = [NotebookRead.from_orm_(nb) for nb in notebooks]
    return notebook_models

@router.get("/notebook_uuid}", response_model=NotebookRead)
def read_notebook(*, session: Session = Depends(get_session), notebook_uuid: str):
    notebook = crud.get_notebook(session, nb_uuid=notebook_uuid)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return NotebookRead.from_orm_(notebook)

@router.delete("/notebook_uuid}")
def delete_notebook(*, session: Session = Depends(get_session), notebook_uuid: str):
    notebook = crud.get_notebook(session, nb_uuid=notebook_uuid)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    session.delete(notebook)
    session.commit()
    return {"ok": True}