from sqlalchemy import Column, ForeignKey, Text, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.database import Base

class NotebookTool(Base):
    __tablename__ = "notebook_tool"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, doc="Display name of the tools. lowercase", index=True)
    description = Column(Text, default=None, doc="Description of the tool")
    homepage = Column(String, doc="Homepage of the tool")
    notebooks = relationship("NotebookToolAssociation", back_populates="tool")


