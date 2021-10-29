from sqlalchemy import Column, ForeignKey, Text, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.database import Base

class NotebookCategory(Base):
    __tablename__ = "notebook_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, doc="Display name of the category", index=True)
    description = Column(Text, doc="Description of the notebook category")
    notebooks = relationship("NotebookCategoryAssociation", back_populates="category")



