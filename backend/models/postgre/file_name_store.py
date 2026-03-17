from sqlalchemy import Column, String, Integer,Date,DateTime
from db.postgre.engine import Base


class UserFiles(Base):
    __tablename__ = "filenamestore"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    time = Column(DateTime, index=True)
    stored_file_name = Column(String, index=True, unique=True)
    original_file_name = Column(String, index=True)

    
    