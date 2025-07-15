from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Base
from sqlalchemy import inspect

#if needed 
#connect_args={'options': '-c timezone=America/Sao_Paulo'})

class PostActions:
    def __init__(self,db_url: str):
        #add echo = True
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def object_as_dict(obj):
        """Converts a SQLAlchemy ORM object to a dictionary."""
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    def add_post(self, post: Post):
        new_post = Post(title=post["title"], description=post["description"], ia_answer=post["ia_answer"], news_url=post["url"])
        print(new_post)
        self.session.add(new_post)
        return self.session.commit()
    
    def create_tables(self):
        return Base.metadata.create_all(self.engine)

    def gest_last_post(self):
        post = self.session.query(Post).order_by(Post.id.desc()).first()
        return post
    
    def get_posts(self):
        posts = self.session.query(Post).all()
        return posts

    def get_post_by_url(self, url: str):
        post = self.session.query(Post).filter(Post.news_url == url).first()
        return post

    def delete_post(self, url: str):
        post = self.session.query(Post).filter(Post.news_url == url).first()
        if post:
            self.session.delete(post)
            self.session.commit()
            return True
        return False

    
#EXAMPLE USAGE
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
postActions = PostActions(DATABASE_URL)
# print(postActions.create_tables())
new_post = {'title':'bueno mija pra cima', 'description': 'qualquer coisa', "ia_answer": 'bueno aloprou','url':'https://buenoalopra.com'}
#add for in loop to get all
#  post = postActions.get_posts()
# print(postActions.object_as_dict(post[0]))


# post = postActions.get_post_by_url('https://buenoalopra.com')
# print(postActions.object_as_dict(post))

# post = postActions.delete_post('https://buenoalopra.com')
# print(post)
