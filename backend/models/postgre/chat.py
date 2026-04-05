from sqlalchemy import ForeignKey, Column, String, Text,Integer, DateTime
from sqlalchemy.orm import relationship
from db.postgre.engine import Base
from datetime import datetime


#one user can have many chats
#one chat can have many messages

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    chat_name = Column(String, index=True)
    
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete")

    
class Message(Base):
    __tablename__ = "message"
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat.id"))

    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

    chat = relationship("Chat", back_populates="messages")
    citations = relationship("Citation", back_populates="message")

    
    
class Citation(Base):
    __tablename__ = "citation"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("message.id"))

    source = Column(String)   
    snippet = Column(String)

    message = relationship("Message", back_populates="citations")