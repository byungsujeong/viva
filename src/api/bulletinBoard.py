from typing import List

from fastapi import APIRouter, Depends, HTTPException

from fastapi_pagination import Page, paginate

from security import get_access_token

from database.orm import BulletinBoard, User
from database.repository import UserRepository, BulletinBoardRepository

from schema.request import BulletinBoardRequest
from schema.response import BulletinBoardSchema, BulletinBoardListResponse, BulletinBoardDetailResponse

from service.userService import UserService


router = APIRouter(prefix="/bbs")


@router.post("/", status_code=201)
def bulletinBoard_post_handler(
    request: BulletinBoardRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repository: UserRepository = Depends(),
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
) -> BulletinBoardSchema:
    user_id: str = user_service.decode_token(token=access_token)
    user: User | None = user_repository.get_user_by_id(user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    bulletinBoard: BulletinBoard = BulletinBoard.create(
        title=request.title,
        contents=request.contents,
        user_id=user_id, 
    )
    bulletinBoard: User = bulletinBoard_repository.create_bulletinBoard(bulletinBoard=bulletinBoard)
    return BulletinBoardSchema.from_orm(bulletinBoard)


@router.get("/", status_code=200)
def get_bulletinBoard_list_handler(
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
) -> Page[BulletinBoardListResponse]:
    bbs: List[BulletinBoard] = bulletinBoard_repository.get_bulletinBoard_list()
    return paginate(bbs)


@router.get("/{bulletinBoard_id}", status_code=200)
def get_bulletinBoard_detail_handler(
    bulletinBoard_id: int,
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
) -> BulletinBoardDetailResponse:
    bulletinBoard: BulletinBoard | None = bulletinBoard_repository.get_bulletinBoard_by_id(bulletinBoard_id=bulletinBoard_id)
    if bulletinBoard:
        if bulletinBoard.updated_at is None:
            bulletinBoard.updated_at = ""
        return BulletinBoardDetailResponse.from_orm(bulletinBoard)
    raise HTTPException(status_code=404, detail="BulletinBoard Not Found")

