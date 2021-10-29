from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional, List

import app.crud.category as crud
from app.api.deps import get_session
from app.schemas.tool import NBToolBase, NBToolCreate, NBToolRead

router = APIRouter()

@router.get("/", response_model=List[NBToolBase])
def read_tools(
    *, session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
    ):
    db_tools = crud.get_all_tools(session, offset, limit)
    return [NBToolBase.from_orm_(db_tool) for db_tool in db_tools]

@router.get("/{tool_id}", response_model=NBToolRead)
def read_tool(
    *,
    session: Session = Depends(get_session),
    tool_id: int 
):
    db_tool = crud.get_tool_byid(session, tool_id)
    tool_model = NBToolRead.from_orm_(db_tool)
    return tool_model

@router.post("/", response_model=NBToolBase)
def create_tool(*, session: Session = Depends(get_session), tool : NBToolCreate):
    db_tool = crud.create_tool(session, tool)
    return db_tool

@router.delete("/{tool_id}")
def delete_tool(*, session: Session = Depends(get_session), tool_id: int):
    db_tool = crud.get_tool_byid(session, tool_id)
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    session.delete(db_tool)
    session.commit()
    return {"ok": True}