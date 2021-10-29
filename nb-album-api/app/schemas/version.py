from typing import List, Optional, Any, Set
from pydantic import BaseModel

class NBVersionBase(BaseModel):
    name: str

class NBVersionRead(NBVersionBase):
    sha256: str
    download_link: str
    default_route: str
    token: str

    class Config:
        orm_mode = True

class NBVersionCreate(NBVersionBase):
    sha256: str
    download_link: str
    default_route: str
    token: str
    notebook_uuid: str
