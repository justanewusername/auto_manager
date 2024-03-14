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
            article = Column(String)
            url = Column(String, nullable=True)

        class Chats(self.Base):
            __tablename__ = "chats"
            id = Column(Integer, primary_key=True)
            chat = Column(String, unique=True)

        self.Post = Posts
        self.Chat = Chats
        self.Base.metadata.create_all(bind=self.engine)

    def create_chat(self, chat_id: str):
        try:
            session = self.SessionLocal()
            new_chat = self.Chat(chat=chat_id)
            session.add(new_chat)

            session.flush()
            session.refresh(new_chat)

            session.expunge_all()
            session.commit()
            session.close()
        except:
            session.rollback()
            return None
        
        return {"id": new_chat.id}
    
    def get_all_chat_id(self):
        session = self.SessionLocal()
        posts = session.query(self.Chat).all()

        result = [record.chat for record in posts]

        session.expunge_all()
        session.close()
        if result is None:
            return None
        return result

    def create_post(self, article: str):
        session = self.SessionLocal()
        new_post = self.Post(article=article)
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