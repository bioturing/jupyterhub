from sqlalchemy import Column, ForeignKey, Text, Integer, String, Time
from sqlalchemy.orm import relationship

from .database import Base

class NotebookCategoryAssociation(Base):
    __tablename__ = 'nb_cat_association'
    notebook_uuid = Column(ForeignKey('notebook_record.uuid'), primary_key=True)
    category_id = Column(ForeignKey('notebook_category.id'), primary_key=True)
    notebook = relationship("NotebookRecord", back_populates="categories")
    category = relationship("NotebookCategory", back_populates="notebooks")

class NotebookToolAssociation(Base):
    __tablename__ = 'nb_tool_association'
    notebook_uuid = Column(ForeignKey('notebook_record.uuid'), primary_key=True)
    tool_id = Column(ForeignKey('notebook_tool.id'), primary_key=True)
    notebook = relationship("NotebookRecord", back_populates="tools")
    tool = relationship("NotebookTool", back_populates="notebooks")

class NotebookCategory(Base):
    __tablename__ = "notebook_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, doc="Display name of the category", index=True)
    description = Column(Text, doc="Description of the notebook category")
    notebooks = relationship("NotebookCategoryAssociation", back_populates="category")

class NotebookTool(Base):
    __tablename__ = "notebook_tool"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, doc="Display name of the tools. lowercase", index=True)
    description = Column(Text, default=None, doc="Description of the tool")
    homepage = Column(String, doc="Homepage of the tool")
    notebooks = relationship("NotebookToolAssociation", back_populates="tool")

class NotebookRecord(Base):
    __tablename__ = "notebook_record"
    uuid = Column(String, doc="UUID of the notebooks. Used to group different version of the notebooks", nullable = False, primary_key=True, index=True)
    name = Column(String, doc="Name of the notebooks", nullable=False, index=True)
    maintainer = Column(String, default=None, doc="Who maintain the notebooks source code", nullable=False)
    source = Column(String, default=None, doc="Where the notebooks hosted. E.g BioTuring Public repo, Private repo")
    description = Column(Text, default=None, doc="Description of the notebook")
    format = Column(String, default=None, doc="Format of the notebook, E.g. IPython, Rmd. Separated by comma")
    time_added: Column(Time, default=None, doc="Time added") 
    time_modified: Column(Time, default=None, doc="Time modified")
    categories = relationship("NotebookCategoryAssociation", back_populates="notebook")
    versions = relationship("NotebookVersion", back_populates="notebook")
    tools = relationship("NotebookToolAssociation", back_populates="notebook")

class NotebookVersion(Base):
    __tablename__ = "notebook_version"
    id = Column(Integer, primary_key=True, index=True)
    sha256 = Column(String, doc="Checksum of the notebook tarball", nullable=False)
    name = Column(String, doc="Version of the notebooks", nullable=False)
    download_link = Column(String, doc="HTTP(s) link to download the notebook tarball", nullable=False)
    default_route = Column(String, default=None, doc="Default notebook show for the end-user after provisioning") 
    token = Column(String, default=None, doc="Environment variable to get the token to download the notebook tarball")
    time_added: Column(Time, default=None, doc="Time added") 
    notebook_uuid = Column(String, ForeignKey('notebook_record.uuid'), doc="Notebook uuid")
    notebook = relationship("NotebookRecord", back_populates="versions")
