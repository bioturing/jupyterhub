from fastapi import APIRouter

from app.api.api_v1.endpoints import notebook, category, tool, version 

api_router = APIRouter()
api_router.include_router(notebook.router, prefix="/notebooks", tags=["notebooks"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(tool.router, prefix="/tools", tags=["tools"])
api_router.include_router(version.router, prefix="/versions", tags=["versions"])