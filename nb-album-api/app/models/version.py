from sqlalchemy import Column, ForeignKey, Text, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.database import Base

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
