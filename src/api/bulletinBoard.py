from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body

from fastapi_pagination import Page, paginate

from security import get_access_token

from database.orm import BulletinBoard, User
from database.repository import UserRepository, BulletinBoardRepository

from schema.request import BulletinBoardRequest, OrderBy, Order
from schema.response import BulletinBoardSchema, BulletinBoardListResponse, BulletinBoardDetailResponse

from service.userService import UserService
from service.bulletinBoardService import BulletinBoardService


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
    orderby: OrderBy,
    order: Order,
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
) -> Page[BulletinBoardListResponse]:
    bbs = bulletinBoard_repository.get_bulletinBoard_list(orderby=orderby, order=order)
    [bb.user.__setattr__('username', '탈퇴한 유저') for bb in bbs if not bb.user.is_active]
    bbs: List[BulletinBoard] = bbs
    return paginate(bbs)


@router.get("/{bulletinBoard_id}", status_code=200)
def get_bulletinBoard_detail_handler(
    bulletinBoard_id: int,
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
    bulletinBoard_service: BulletinBoardService = Depends(),
) -> BulletinBoardDetailResponse:
    bulletinBoard: BulletinBoard | None = bulletinBoard_repository.get_bulletinBoard_by_id(bulletinBoard_id=bulletinBoard_id)
    if not bulletinBoard:
        raise HTTPException(status_code=404, detail="BulletinBoard Not Found")
    
    bulletinBoard = bulletinBoard_service.replace_field(bulletinBoard=bulletinBoard)
    
    return BulletinBoardDetailResponse.from_orm(bulletinBoard)


@router.patch("/{bulletinBoard_id}", status_code=200)
def update_bulletinBoard_handler(
    bulletinBoard_id: int,
    request: BulletinBoardRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
) -> BulletinBoardDetailResponse:
    bulletinBoard: BulletinBoard | None = bulletinBoard_repository.get_bulletinBoard_by_id(bulletinBoard_id=bulletinBoard_id)
    if not bulletinBoard:
        raise HTTPException(status_code=404, detail="BulletinBoard Not Found")
    
    user_id: str = user_service.decode_token(token=access_token)
    if bulletinBoard.user_id != int(user_id):
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    bulletinBoard.update(request=request)
    bulletinBoard: BulletinBoard = bulletinBoard_repository.update_bulletinBoard(bulletinBoard=bulletinBoard)
    return BulletinBoardDetailResponse.from_orm(bulletinBoard)


@router.delete("/{bulletinBoard_id}", status_code=204)
def delete_bulletinBoard_handler(
    bulletinBoard_id: int,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    bulletinBoard_repository: BulletinBoardRepository = Depends(),
):
    bulletinBoard: BulletinBoard | None = bulletinBoard_repository.get_bulletinBoard_by_id(bulletinBoard_id=bulletinBoard_id)
    if not bulletinBoard:
        raise HTTPException(status_code=404, detail="BulletinBoard Not Found")
    
    user_id: str = user_service.decode_token(token=access_token)
    if bulletinBoard.user_id != int(user_id):
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    bulletinBoard_repository.delete_bulletinBoard(bulletinBoard_id=bulletinBoard_id)
