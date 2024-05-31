from fastapi import APIRouter, Depends, HTTPException

from schema.request import SignUpRequest, LogInRequest, UserUpdateRequest
from schema.response import UserSchema, JWTResponse

from database.repository import UserRepository
from database.orm import User

from service.userService import UserService

from security import get_access_token


router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(UserService),
    user_repository: UserRepository = Depends(UserRepository),
) -> UserSchema:
    
    user: User | None = user_repository.get_user_by_email(email=request.email)
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


@router.post("/log-in", status_code=201)
def user_log_in_handler(
    request: LogInRequest,
    user_repository: UserRepository = Depends(UserRepository),
    user_service: UserService = Depends(),
):

    user: User | None = user_repository.get_user_by_email(email=request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    verified: bool = user_service.verify_password(
        password=request.password,
        hashed_password=user.password,
    )

    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    access_token: str = user_service.create_access_token(user)
    refresh_token: str = user_service.create_refresh_token(user)

    return JWTResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", status_code=200)
def get_user_handler(
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repository: UserRepository = Depends(),
) -> UserSchema:
    user_id: str = user_service.decode_token(token=access_token)
    user: User | None = user_repository.get_user_by_id(user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return UserSchema.from_orm(user)



@router.patch("/me", status_code=200)
def update_user_handler(
    request: UserUpdateRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repository: UserRepository = Depends(),
) -> UserSchema:
    user_id: str = user_service.decode_token(token=access_token)
    if request.id != int(user_id):
        raise HTTPException(status_code=401, detail="Not Authorized")
    user: User | None = user_repository.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    verified: bool = user_service.verify_password(
        password=request.password,
        hashed_password=user.password,
    )
    
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    hashed_password: str | None = user_service.hash_password(
        password=request.new_password,
    )
    user: User = user_repository.update_user(
        user=user,
        username=request.username,
        password=hashed_password,
    )
    return UserSchema.from_orm(user)
