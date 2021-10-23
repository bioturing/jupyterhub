from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import os

Base = declarative_base()

class NBProvisionRecord(Base):
    __tablename__ = 'nb_provision_records'

    useremail = Column(Text, nullable=False)
    envname = Column(Text, nullable=True)
    uid = Column(Text, primary_key=True)
    progress = Column(Integer, default=0)
    notebookname = Column(Text, nullable=True)
    logmess = Column(Text, nullable=True)
    status = Column(String(32), nullable=False)

    def to_dict(self):
        """Return a dictionary representation of this model."""
        return {
            "logmess": self.logmess,
            "status": self.status,
            "notebookname": self.notebookname,
            "progress": self.progress,
            "useremail" : self.useremail,
            "envname" : self.envname
        }

dbfile = f"{os.environ['HOME']}/.nb-provision.db"
engine = create_engine(f'sqlite:///{dbfile}', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
