import os
import json

from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session

from setting import NB_DB_DIR
from orm.database import SessionLocal, engine
from orm import models, crud, schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

"""
Notebook APIs
"""
@app.post("/notebooks/", response_model=schemas.NotebookRead)
def create_notebook(*, session: Session = Depends(get_session), nb: schemas.NotebookCreate):
    db_notebook_maybe = crud.get_notebook(session, nb.uuid)
    if db_notebook_maybe:
        raise HTTPException(status_code=400, detail="Notebook already existed")
    db_notebook = crud.create_notebook(session, nb)
    notebook_model = schemas.NotebookRead.from_orm_(db_notebook)
    return notebook_model

@app.get("/notebooks/", response_model=List[schemas.NotebookRead])
def read_notebooks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    notebooks = crud.get_all_notebooks(session, offset, limit) 
    notebook_models = [schemas.NotebookRead.from_orm_(nb) for nb in notebooks]
    return notebook_models

@app.get("/notebooks/{notebook_uuid}", response_model=schemas.NotebookRead)
def read_notebook(*, session: Session = Depends(get_session), notebook_uuid: str):
    notebook = crud.get_notebook(session, nb_uuid=notebook_uuid)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return schemas.NotebookRead.from_orm_(notebook)

@app.delete("/notebooks/{notebook_uuid}")
def delete_notebook(*, session: Session = Depends(get_session), notebook_uuid: str):
    notebook = crud.get_notebook(session, nb_uuid=notebook_uuid)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    session.delete(notebook)
    session.commit()
    return {"ok": True}

"""
Categories API
"""

@app.get("/categories/{category_id}", response_model=schemas.NBCategoryRead)
def read_category(
    *,
    session: Session = Depends(get_session),
    category_id: int
):
    db_category = crud.get_category_byid(session, category_id)
    cat_model = schemas.NBCategoryRead.from_orm_(db_category)
    return cat_model

@app.get("/categories/", response_model=List[schemas.NBCategoryBase])
def read_categories(
    *, session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
    ):
    db_categories = crud.get_all_categories(session, offset, limit)
    return [schemas.NBCategoryBase.from_orm_(db_cat) for db_cat in db_categories]

@app.post("/categories/", response_model=schemas.NBCategoryBase)
def create_category(*, session: Session = Depends(get_session), cat : schemas.NBCategoryCreate):
    db_category = crud.create_category_byname(session, **cat.dict())
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = crud.get_category_byid(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}

"""
Tools API
"""

@app.get("/tools/", response_model=List[schemas.NBToolBase])
def read_tools(
    *, session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
    ):
    db_tools = crud.get_all_tools(session, offset, limit)
    return [schemas.NBToolBase.from_orm_(db_tool) for db_tool in db_tools]

@app.get("/tools/{tool_id}", response_model=schemas.NBToolRead)
def read_tool(
    *,
    session: Session = Depends(get_session),
    tool_id: int 
):
    db_tool = crud.get_tool_byid(session, tool_id)
    tool_model = schemas.NBToolRead.from_orm_(db_tool)
    return tool_model

@app.post("/tools/", response_model=schemas.NBToolBase)
def create_tool(*, session: Session = Depends(get_session), tool : schemas.NBToolCreate):
    db_tool = crud.create_tool(session, tool)
    return db_tool

@app.delete("/tools/{tool_id}")
def delete_tool(*, session: Session = Depends(get_session), tool_id: int):
    db_tool = crud.get_tool_byid(session, tool_id)
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    session.delete(db_tool)
    session.commit()
    return {"ok": True}

"""
Notebook version API
"""

@app.post("/notebooks/versions/", response_model=schemas.NBVersionRead)
def create_notebook_version(*, session: Session = Depends(get_session), nbversion: schemas.NBVersionCreate):
    db_notebook = crud.get_notebook(session, nbversion.notebook_uuid)
    if not db_notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    db_nbversion_maybe = crud.get_notebook_version(session, nbversion.notebook_uuid, nbversion.name)
    if db_nbversion_maybe:
        raise HTTPException(status_code=400, detail="Version already existed")
    db_nbversion = crud.create_notebook_version(session, nbversion)
    return db_nbversion

@app.get("/notebooks/versions/{notebook_uuid}", response_model=List[schemas.NBVersionRead])
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

@app.delete("/notebooks/versions/{notebook_uuid}/{version_id}")
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