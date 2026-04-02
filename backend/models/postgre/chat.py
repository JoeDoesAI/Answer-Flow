from sqlalchemy import Column, String,Integer, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from db.postgre.engine import Base
from datetime import datetime


#one user can have many chats
#one chat can have many messages

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    chat_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="user")
    messages = relationship("Message", back_populates="chat", cascade="all, delete")

    
class UserMessage(Base):
    __tablename__ = "messages"
    
    query = Column(String, index=True)
    reply = Column(String, index=True)
    citation = Column(String, index=True)
    chat_id = Column(Integer, ForeignKey("chat.id"))
    timestamp = Column(DateTime, default=datetime.now)

    chat = relationship("Chat", back_populates="messages")
    
class Citation(Base):
    __tablename__ = "citations"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"))

    source = Column(String)   
    snippet = Column(String)
