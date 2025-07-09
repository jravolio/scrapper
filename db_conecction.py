from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Date
from datetime import date
#would be better to create a new file just for the imports? 

#i literally have no idea if this is the right URL, i just tought it would be the conecction host
#"jdbc:postgresql://localhost:5432/postgres" 
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)
session = session()
#esse base = declarative_base() aqui foi o copilot q me safou
Base = declarative_base()
#alr created the table at dbeaver, will create another one here just so i can test the code
class Post(Base):
    __tablename__ = "post"
    title = Column(String(100))
    description = Column(String(250))
    post_date = Column(Date)
    news_url = Column(String(100), primary_key=True)
    ia_answer = Column(String(280))
#copilot describe it to help identify the title and url as string, necessary indeed or nah?
    def __repr__(self):
        return f"<Post(title={self.title}, url={self.news_url})>"
Base.metadata.create_all(engine)
    
example_post = Post(
     title = "example tittle",
	description = 'example description',
    post_date = date.today(),
    news_url = "https://naoseioquetofazendomastoseguindoalibrary.com.fudeu",
    ia_answer = 'se isso fechar a conexão deve inserir na tabela se não eu vou dormir'
)
#learnt quite late that you have to commit as you usually would with dbeaver
try:
    session.add(example_post)
    session.commit()
    print("Post inserted successfully.")
except Exception as e:
    session.rollback()
    print("Error inserting post:", e)
finally:
    session.close()
