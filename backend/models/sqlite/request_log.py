from sqlalchemy import Column, Integer, String
from db.sqlite.engine import Base


class RequestLog(Base):
    __tablename__ = "request_log"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)
    method = Column(String, index=True)
    url = Column(String, index=True)
    status_code = Column(String, index=True)
    client_ip = Column(String, index=True)