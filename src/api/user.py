from fastapi import APIRouter, Depends, HTTPException

from schema.request import SignUpRequest
from schema.response import UserSchema

from database.repository import UserRepository
from database.orm import User

from service.userService import UserService


router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(UserService),
    user_repository: UserRepository = Depends(UserRepository),
) -> UserSchema:
    
    user: User | None = user_repository.get_user_by_email(email=request.email)
    print(user)
    if user:
        raise HTTPException(status_code=409, detail="Already Registered Email")

    hashed_password: str = user_service.hash_password(
        password=request.password,
    )
    new_user: User = User.create(
        email=request.email,
        hashed_password=hashed_password,
        username=request.username,
    )
    new_user: User = user_repository.create_user(user=new_user)
    return UserSchema.from_orm(new_user)