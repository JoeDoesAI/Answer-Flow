from sqlalchemy import Column, String, Integer
from db.postgre.engine import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String(255), index=True)

    chats = relationship("Message", back_populates="owner")
    files = relationship("File", back_populates="owner")

