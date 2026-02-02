from sqlalchemy import Column, String, Integer
from db.sqlite.engine import Base



class QueryLog(Base):
    __tablename__  = "query_log"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    time =  Column(String, index=True)
    query_text = Column(String, index=True)
    query_length = Column(Integer, index=True)
    response = Column(String, index=True)
    response_length = Column(String, index=True)
    