from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

        # Определение модели данных (ORM)
        class Posts(self.Base):
            __tablename__ = "items"
            id = Column(Integer, primary_key=True)
            article = Column(String, unique=True)
            title = Column(String, nullable=True)
            url = Column(String, nullable=True)

        self.Post = Posts
        self.Base.metadata.create_all(bind=self.engine)

    def create_post(self, article: str, title: str, url: str):
        session = self.SessionLocal()
        new_post = self.Post(article=article, title=title, url=url)
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