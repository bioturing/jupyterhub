import os
import json

from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from setting import NB_DB_DIR
from orm import NotebookRecordCreate, NotebookRecordRead, NotebookRecord, NotebookCategory, sqlite_url

from sqlmodel import Session, SQLModel, create_engine, select

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/notebooks/", response_model=NotebookRecordRead)
def create_notebook(*, session: Session = Depends(get_session), nb: NotebookRecordCreate):
    db_notebook = NotebookRecord.from_orm(nb)
    db_notebook.time_added = datetime.now()
    session.add(db_notebook)
    session.commit()
    session.refresh(db_notebook)
    return db_notebook

@app.post("/categories/", response_model=NotebookCategory)
def create_category(*, session: Session = Depends(get_session), cat : NotebookCategory):
    db_category = NotebookCategory.from_orm(cat)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@app.get("/notebooks/", response_model=List[NotebookRecordRead])
def read_notebooks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    notebooks = session.exec(select(NotebookRecord).offset(offset).limit(limit)).all()
    return notebooks

@app.get("/notebooks/{notebook_id}", response_model=NotebookRecordRead)
def read_notebook(*, session: Session = Depends(get_session), notebook_id: int):
    notebook = session.get(NotebookRecord, notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook

@app.delete("/notebooks/{notebook_id}")
def delete_notebook(*, session: Session = Depends(get_session), notebook_id: int):

    notebook = session.get(NotebookRecord, notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    session.delete(notebook)
    session.commit()
    return {"ok": True}
