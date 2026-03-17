from sqlalchemy import Column, String,Integer, DateTime,ForeignKey
from db.postgre.engine import Base
from datetime import datetime




class UserChat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    chat_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.now)


class UserMessage(Base):
    __tablename__ = "messages"

    
    query = Column(String, index=True)
    reply = Column(String, index=True)
    citation = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.now)



