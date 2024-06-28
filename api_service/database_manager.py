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

        class TelegramUsers(self.Base):
            __tablename__ = "telegram_users"
            id = Column(Integer, primary_key=True)
            telegram_user_id = Column(Integer, nullable=False, unique=True)


        class Answers(self.Base):
            __tablename__ = "answers"
            id = Column(Integer, primary_key=True)
            post_id = Column(Integer, ForeignKey("posts.id"), unique=False)
            answer = Column(String, nullable=False)


        class PostsMessages(self.Base):
            __tablename__ = "posts_messages"
            id = Column(Integer, primary_key=True)
            post_id = Column(Integer, ForeignKey("posts.id"), unique=False)
            message_id = Column(Integer, unique=True)


        class Favorites(self.Base):
            __tablename__ = "favorites"
            id = Column(Integer, primary_key=True)
            post_id = Column(Integer, ForeignKey("posts.id"), unique=True)
    
            __table_args__ = (
                UniqueConstraint('post_id'),
            )

        self.Post = Posts
        self.Answers = Answers
        self.PostsMessages = PostsMessages
        self.TelegramUser = TelegramUsers
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

        posts = session.query(self.Post, exists().where(self.Favorites.post_id == self.Post.id).label('in_favorites')).limit(13).all()

        session.expunge_all()
        session.close()
        if posts is None:
            return None

        posts_list = []
        for item in posts:
            dict_item = {**item[0].__dict__, 'in_favorites': item.in_favorites}
            posts_list.append(dict_item)
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


    # TELEGRAM USER
    def create_telegram_user(self, telegram_user_id: int):
        session = self.SessionLocal()
        try:
            new_user = self.TelegramUser(telegram_user_id=telegram_user_id)
            session.add(new_user)

            session.flush()
            session.refresh(new_user)

            session.expunge_all()
            session.commit()
            session.close()
            return {"id": new_user.id}
        except:
            session.close()
            return None
    

    def check_telegram_user_by_id(self, telegram_user_id: int):
        session = self.SessionLocal()
        try:
            telegram_user = session.query(self.TelegramUser).filter(self.TelegramUser.telegram_user_id == telegram_user_id).first()
            session.expunge_all()
            session.close()
            if telegram_user is None:
                return False
            return True
        except:
            session.close()

    
    def get_all_telegram_users(self):
        session = self.SessionLocal()

        telegram_users = session.query(self.TelegramUser).all()

        session.expunge_all()
        session.close()
        if telegram_users is None:
            return None

        telegram_users_list = []
        for item in telegram_users:
            telegram_users_list.append(item.telegram_user_id)
        return telegram_users_list
    
    def delete_telegram_user(self, user_id: int):
        session = self.SessionLocal()
        try:
            user_to_delete = session.query(self.TelegramUser).filter_by(user_id=user_id).first()

            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
                return {"message": f"Telegram user with user_id {user_id} deleted successfully"}
            else:
                return {"message": f"No telegram user found with {user_id}"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # TELEGRAM MESSAGES AND ANSWERS

    def add_message_id(self, post_id: int, message_id: int):
        session = self.SessionLocal()
        try:
            new_post_message = self.PostsMessages(post_id=post_id, message_id=message_id)
            session.add(new_post_message)
            
            session.flush()
            session.refresh(new_post_message)

            session.expunge_all()
            session.commit()
        except:
            pass
        session.close()
        return
    

    def get_post_id_by_message_id(self, message_id: int):
        session = self.SessionLocal()
        try:
            post_message = session.query(self.PostsMessages).filter(self.PostsMessages.message_id == message_id).first()
            session.expunge_all()
            session.close()
            if post_message is None:
                return None
            return post_message.post_id
        except:
            session.close()
    

    def add_answer(self, post_id: int, answer: str):
        session = self.SessionLocal()
        try:
            new_answwer = self.Answers(post_id=post_id, answer=answer)
            session.add(new_answwer)

            session.flush()
            session.refresh(new_answwer)

            session.expunge_all()
            session.commit()
        except:
            pass
        finally:
            session.close()
        return


    def delete_answer(self, answer_id: int):
        session = self.SessionLocal()
        try:
            answer_to_delete = session.query(self.Answers).filter_by(id=answer_id).first()

            if answer_to_delete:
                session.delete(answer_to_delete)
                session.commit()
                return {"message": f"Telegram user with user_id {answer_id} deleted successfully"}
            else:
                return {"message": f"No telegram user found with {answer_id}"}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_answers(self):
        session = self.SessionLocal()
        try:
            answers = session.query(self.Answers, self.Post, self.Post.url).join(self.Post, self.Post.id == self.Answers.post_id).all()

            session.expunge_all()
            session.close()

            if answers is None:
                return None
            
            answers_list = [
                {
                    'answer_id': answer.id,
                    'answer': answer.answer,
                    'post_title': title,
                    'post_url': url
                }
                for answer, title, url in answers
            ]

            return answers_list
        except Exception as e:
            print('some error:', e)
            session.close()
        return None