from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

        # Определение модели данных (ORM)
        class Posts(self.Base):
            __tablename__ = "posts"
            id = Column(Integer, primary_key=True)
            article =  Column(String(32000), nullable=True) #Column(String, unique=True)
            title = Column(String, nullable=True)
            url = Column(String, nullable=True)
            category = Column(String, nullable=True)
            resource = Column(String, nullable=True)
            last_update = Column(String, nullable=True)

        # class Titles(self.Base):
        #     __tablename__ = "titles"
        #     id = Column(Integer, primary_key=True)
        #     title = Column(String, nullable=False)
        #     url = Column(String, nullable=False)
        #     category = Column(String, nullable=False)
        #     resource = Column(String, nullable=False)
        #     last_update = Column(String, nullable=True)
        
        self.Post = Posts
        # self.Title = Titles
        self.Base.metadata.create_all(bind=self.engine)

    # # TITLES
    # def create_title(self, title: str, url: str, category: str, resource: str, last_update: str):
    #     session = self.SessionLocal()
    #     new_title = self.Title(title=title, url=url, category=category, resource=resource, last_update=last_update)
    #     session.add(new_title)
        
    #     session.flush()
    #     session.refresh(new_title)

    #     session.expunge_all()
    #     session.commit()
    #     session.close()
        
    #     return {"id": new_title.id}


    # POSTS
    def create_post(self, title: str, url: str, article: str = None):
        today = datetime.today()
        formatted_date = today.strftime('%d.%m.%Y')

        session = self.SessionLocal()
        new_post = self.Post(
            title=title,
            url=url,
            article=article,
            last_update=formatted_date
        )
        session.add(new_post)

        session.flush()
        session.refresh(new_post)

        session.expunge_all()
        session.commit()
        session.close()

        return {"id": new_post.id}

    def get_post_by_id(self, post_id: int):
        session = self.SessionLocal()
        post = session.query(self.Post).filter(self.Post.id == post_id).first()
        session.expunge_all()
        session.close()
        if post is None:
            return None
        return post
    

    def get_post_by_article(self, article: str):
        session = self.SessionLocal()
        post = session.query(self.Post).filter(self.Post.article == article).first()
        session.expunge_all()
        session.close()
        if post is None:
            return None
        return post
    
    def get_all_posts(self):
        session = self.SessionLocal()
        posts = session.query(self.Post).all()
        session.expunge_all()
        session.close()
        if posts is None:
            return None
        posts_list = [post.__dict__ for post in posts]
        return posts_list