from typing import List

from fastapi import Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import User, BulletinBoard

from schema.request import OrderBy, Order


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
    
    def update_user(self, user: User) -> User:
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
    
    def get_bulletinBoard_list(self, orderby: str, order: str) -> List[BulletinBoard]:
        if orderby==OrderBy.hits:
            if order==Order.asc:
                return list(self.session.scalars(select(BulletinBoard).order_by(BulletinBoard.hits.asc())))
            else:
                return list(self.session.scalars(select(BulletinBoard).order_by(BulletinBoard.hits.desc())))
        
        if order==Order.asc:
            return list(self.session.scalars(select(BulletinBoard).order_by(BulletinBoard.created_at.asc())))
        else:
            return list(self.session.scalars(select(BulletinBoard).order_by(BulletinBoard.created_at.desc())))
    
    
    def get_bulletinBoard_by_id(self, bulletinBoard_id: int) -> BulletinBoard | None:
        return self.session.scalar(select(BulletinBoard).where(BulletinBoard.id == bulletinBoard_id))
    
    def update_bulletinBoard(self, bulletinBoard: BulletinBoard) ->  BulletinBoard:
        self.session.add(instance=bulletinBoard)
        self.session.commit()
        self.session.refresh(instance=bulletinBoard)
        return bulletinBoard
    
    def delete_bulletinBoard(self, bulletinBoard_id: int) -> None:
        self.session.execute(delete(BulletinBoard).where(BulletinBoard.id == bulletinBoard_id))
        self.session.commit()
