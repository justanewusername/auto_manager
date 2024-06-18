from sqlalchemy import create_engine, Column, Integer, String, or_, ForeignKey, UniqueConstraint, exists
from sqlalchemy.orm import sessionmaker, mapped_column
from sqlalchemy.ext.declarative import declarative_base


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

        class Users(self.Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
            email = Column(String, nullable=False)
            password = Column(String, nullable=False)
            websocket_connection = Column(String, nullable=True)

        class Favorites(self.Base):
            __tablename__ = "favorites"
            id = Column(Integer, primary_key=True)
            post_id = Column(Integer, ForeignKey("posts.id"), unique=True)
    
            __table_args__ = (
                UniqueConstraint('post_id'),
            )

        self.Post = Posts
        self.Favorites = Favorites
        self.Users = Users
        self.Base.metadata.create_all(bind=self.engine)

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
    
    def get_all_posts(self):
        session = self.SessionLocal()

        posts = session.query(self.Post, exists().where(self.Favorites.post_id == self.Post.id).label('in_favorites')).limit(10).all()

        session.expunge_all()
        session.close()
        if posts is None:
            return None

        posts_list = []
        for item in posts:
            dict_item = {**item[0].__dict__, 'in_favorites': item.in_favorites}
            posts_list.append(dict_item)

        # posts_list = [post.__dict__ for post in posts]
        return posts_list

    def delete_all_posts(self):
        session = self.SessionLocal()
        try:
            session.query(self.Post).delete()
            session.commit()
            return {"message": "All posts deleted successfully"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_post_by_identifier(self, identifier: str):
        session = self.SessionLocal()
        try:
            filter_condition = or_(self.Post.article == identifier, self.Post.url == identifier)
            post_to_delete = session.query(self.Post).filter(filter_condition).first()

            if post_to_delete:
                session.delete(post_to_delete)
                session.commit()
                return {"message": f"Post with {identifier} deleted successfully"}
            else:
                return {"message": f"No post found with {identifier}"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_post_by_id(self, post_id: int):
        session = self.SessionLocal()
        try:
            post_to_delete = session.query(self.Post).filter(self.Post.id == post_id).first()

            if post_to_delete:
                session.delete(post_to_delete)
                session.commit()
                return {"message": f"Post with {post_id} deleted successfully"}
            else:
                return {"message": f"No post found with {post_id}"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_to_favorites(self, post_id: int):
        session = self.SessionLocal()
        new_favorite = self.Favorites(post_id = post_id)
        session.add(new_favorite)
        
        session.flush()
        session.refresh(new_favorite)

        session.expunge_all()
        session.commit()
        session.close()
        
        return {"id": new_favorite.id}
    
    def delete_from_favorites(self, favorite_id: int):
        session = self.SessionLocal()
        try:
            favorite_to_delete = session.query(self.Favorites).filter(self.Favorites.post_id == favorite_id).first()

            if favorite_to_delete:
                session.delete(favorite_to_delete)
                session.commit()
                return True #{"message": f"Post with id {favorite_id} deleted successfully from favorites"}
            else:
                return False #{"message": f"No post found with id {favorite_id} in favorites"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_favorites(self):
        session = self.SessionLocal()

        posts = session.query(self.Post, exists().where(self.Favorites.post_id == self.Post.id).label('in_favorites')).all()

        session.expunge_all()
        session.close()
        if posts is None:
            return None

        posts_list = []
        for item in posts:
            dict_item = {**item[0].__dict__, 'in_favorites': item.in_favorites}
            if dict_item["in_favorites"] == False:
                continue
            posts_list.append(dict_item)

        return posts_list
    

####### USER

    def create_user(self, email: str, password: str):
        session = self.SessionLocal()
        new_user = self.Users(password = password, email = email)
        session.add(new_user)
        
        session.flush()
        session.refresh(new_user)

        session.expunge_all()
        session.commit()
        session.close()
        
        return {"id": new_user.id}
    

    def get_user_by_id(self, user_id: int):
        session = self.SessionLocal()
        user = session.query(self.Users).filter(self.Users.id == user_id).first()
        session.expunge_all()
        session.close()
        if user is None:
            return None
        return user

    def get_user_by_email(self, user_email: str):
        session = self.SessionLocal()
        user = session.query(self.Users).filter(self.Users.email == user_email).first()
        session.expunge_all()
        session.close()
        if user is None:
            return None
        data = {
            'id': user.id,
            'email': user.email,
            'password': user.password,
        }
        return data


    def get_websocket_connection_by_id(self, user_id: int):
        session = self.SessionLocal()
        user = session.query(self.Users).filter(self.Users.id == user_id).first()
        session.expunge_all()
        session.close()
        if user is None:
            return None
        return user.websocket_connection

    def update_websocket_connection_by_id(self, user_id: int, connection: str):
        session = self.SessionLocal()
        try:
            user = session.query(self.Users).filter_by(id=user_id).first()
            if user:
                user.websocket_connection = connection
                session.commit()
                return {"message": "Connection updated successfully"}
            else:
                return {"message": "User not found"}
        except Exception as e:
            session.rollback()
            return {"message": str(e)}
        finally:
            session.close()

    def update_websocket_connection_by_email(self, user_email: str, connection: str):
        session = self.SessionLocal()
        try:
            user = session.query(self.Users).filter_by(email=user_email).first()
            if user:
                user.websocket_connection = connection
                session.commit()
                return {"message": "Connection updated successfully"}
            else:
                return {"message": "User not found"}
        except Exception as e:
            session.rollback()
            return {"message": str(e)}
        finally:
            session.close()