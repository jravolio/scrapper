from sqlalchemy import Column, String, Text
from sqlalchemy.orm import declarative_base
from datetime import date
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = "post"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(300))
    description = Column(Text)
    created_at = Column(DateTime(timezone= True), server_default= func.now())
    news_url = Column(String(300), primary_key=True)
    ai_title = Column(String(280)) # max length for Twitter
    tweet_id = Column(BigInteger, nullable=True)

    def __init__(self, title, description, news_url, ai_title, tweet_id=None):
        self.title = title
        self.description = description
        self.news_url = news_url
        self.ai_title = ai_title
        self.tweet_id = tweet_id
    
    