from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.post import Post, Base
from sqlalchemy import inspect

#if needed 
#connect_args={'options': '-c timezone=America/Sao_Paulo'})

class PostActions:
    """
    Provides actions for managing Post records in the database using SQLAlchemy.
    Args:
        db_url (str): The database connection URL.
    Attributes:
        engine: SQLAlchemy engine instance connected to the database.
        session: SQLAlchemy session for performing database operations.
    Methods:
        object_as_dict(obj): Converts a SQLAlchemy ORM object to a dictionary.
        add_post(post): Adds a new post to the database.
        create_tables(): Creates all tables defined in the SQLAlchemy Base metadata.
        gest_last_post(): Retrieves the most recently added post.
        get_posts(): Retrieves all posts from the database.
        get_post_by_url(url): Retrieves a post by its news URL.
        delete_post(url): Deletes a post by its news URL.
    """

    def __init__(self,db_url: str):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def object_as_dict(obj):
        """Converts a SQLAlchemy ORM object to a dictionary."""
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def add_post(self, title: str, description: str, ai_title: str, news_url: str, tweet_id: int = None):
        new_post = Post(title=title, description=description, ai_title=ai_title, news_url=news_url, tweet_id=tweet_id)
        self.session.add(new_post)
        self.session.commit()
        return new_post
    
    def create_tables(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        if 'posts' not in tables:
            Base.metadata.create_all(self.engine)

    def gest_last_post(self):
        post = self.session.query(Post).order_by(Post.id.desc()).first()
        return post
    
    def get_posts(self):
        posts = self.session.query(Post).all()
        return posts

    def get_post_by_url(self, url: str):
        post = self.session.query(Post).filter_by(news_url=url).first()
        return post

    def delete_post(self, url: str):
        post = self.session.query(Post).filter_by(news_url=url).first()
        if post:
            self.session.delete(post)
            self.session.commit()
            return True
        return False

    
#EXAMPLE USAGE
# DATABASE_URL = "your_database_url_here"  # Replace with your actual database URL
# postActions = PostActions(DATABASE_URL)
# new_post = {
#     'title': 'AI Revolutionizes News Reporting',
#     'description': 'A detailed look at how artificial intelligence is transforming the journalism industry, from automated content creation to personalized news feeds.',
#     'ai_title': 'AI enables faster, more accurate news delivery and helps journalists focus on in-depth analysis.',
#     'url': 'https://news.example.com/ai-revolution-news-reporting'
# }

#add_post 
# post = postActions.add_post(new_post)
# print(postActions.object_as_dict(post))

#get_last_post
# post = postActions.gest_last_post()
# print(postActions.object_as_dict(post))

#get_posts
# posts = postActions.get_posts()
# for post in posts:
#     print(postActions.object_as_dict(post))

#get_posts_by_url
# post = postActions.get_post_by_url('PasteURL')
# print(postActions.object_as_dict(post))

#delete_post
# post = postActions.delete_post('PasteURL')
# print(post)
