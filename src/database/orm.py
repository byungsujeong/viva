from sqlalchemy import (
    Boolean, Column, Integer, String,
    DateTime, Text, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=func.current_timestamp())


class User(Base, BaseMixin):
    __tablename__ = "user"

    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    username = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    leave_date = Column(DateTime, default=None, nullable=True)
    # created_at: join date

    bulletinBoards = relationship("BulletinBoard", lazy="joined")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, username={self.username}, is_active={self.is_active})"
    
    @classmethod
    def create(cls, email: str, hashed_password: str, username: str) -> "User":
        return cls(
            email=email,
            password=hashed_password,
            username=username,
        )

    
class BulletinBoard(Base, BaseMixin):
    __tablename__ = "bulletinBoard"

    title = Column(String(100), nullable=False)
    contents = Column(Text, nullable=False)
    hits = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("user.id"))
    # created_at: post date
    # updated_at: update date

    user = relationship("User", back_populates="bulletinBoards")
    
    @classmethod
    def create(cls, title: str, contents, user_id: int) -> "BulletinBoard":
        return cls(
            title=title,
            contents=contents,
            user_id=user_id, 
        )


# from sqlalchemy.schema import CreateTable
# from database.connection import engine
# print(CreateTable(User.__table__).compile(engine))
# print(CreateTable(BulletinBoard.__table__).compile(engine))