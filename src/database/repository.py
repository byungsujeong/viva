from typing import List

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import User, BulletinBoard


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))
    
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.scalar(select(User).where(User.id == user_id))
    
    def update_user(self, user: User, username: str, password: str) -> User:
        user.username = username
        if password:
            user.password = password
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user
    

class BulletinBoardRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_bulletinBoard(self, bulletinBoard: BulletinBoard) ->  BulletinBoard:
        self.session.add(instance=bulletinBoard)
        self.session.commit()
        self.session.refresh(instance=bulletinBoard)
        return bulletinBoard
    
    def get_bulletinBoard_list(self) -> List[BulletinBoard]:
        return list(self.session.scalars(select(BulletinBoard)))
    
    def get_bulletinBoard_by_id(self, bulletinBoard_id: int) -> BulletinBoard | None:
        return self.session.scalar(select(BulletinBoard).where(BulletinBoard.id == bulletinBoard_id))
    
    def update_bulletinBoard(self, bulletinBoard: BulletinBoard) ->  BulletinBoard:
        self.session.add(instance=bulletinBoard)
        self.session.commit()
        self.session.refresh(instance=bulletinBoard)
        return bulletinBoard