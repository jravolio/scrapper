from sqlalchemy import Column, String, Date, engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = "post"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(250))
    created_at = Column(DateTime(timezone= True), server_default= func.now())
    news_url = Column(String(100), primary_key=True)
    ia_answer = Column(String(280))

    def __init__(self, title, description, news_url, ia_answer):
        self.title = title
        self.description = description
        self.news_url = news_url
        self.ia_answer = ia_answer
    
    