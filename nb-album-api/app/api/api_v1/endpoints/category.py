from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional, List

import app.crud.category as crud
from app.api.deps import get_session
from app.schemas.category import NBCategoryRead, NBCategoryBase, NBCategoryCreate

router = APIRouter()

@router.get("/{category_id}", response_model=NBCategoryRead)
def read_category(
    *,
    session: Session = Depends(get_session),
    category_id: int
):
    db_category = crud.get_category_byid(session, category_id)
    cat_model = NBCategoryRead.from_orm_(db_category)
    return cat_model

@router.get("/", response_model=List[NBCategoryBase])
def read_categories(
    *, session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
    ):
    db_categories = crud.get_all_categories(session, offset, limit)
    return [NBCategoryBase.from_orm_(db_cat) for db_cat in db_categories]

@router.post("/", response_model=NBCategoryBase)
def create_category(*, session: Session = Depends(get_session), cat : NBCategoryCreate):
    db_category = crud.create_category_byname(session, **cat.dict())
    return db_category

@router.delete("/{category_id}")
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = crud.get_category_byid(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}