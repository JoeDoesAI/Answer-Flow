from sqlalchemy import Column, String, Integer,Date,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from db.postgre.engine import Base


class Files(Base):
    __tablename__ = "file"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date, index=True)
    timestamp = Column(DateTime, index=True)
    original_name = Column(String, index=True)
    stored_name = Column(String, index=True, unique=True)

    user = relationship("User", back_populates="user")
    
    