from sqlalchemy import Column, String, Integer
from db.sqlite.engine import Base


class FileNameStore(Base):
    __tablename__ = "filenamestore"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)
    stored_file_name = Column(String, index=True, unique=True)
    original_file_name = Column(String, index=True)
    