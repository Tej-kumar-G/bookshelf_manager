# app/routes/users.py
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.users import CreateUser, UpdateUser, UserResponse, BaseUserResponse
from app.services.users import UserService
from app.database import get_database

router = APIRouter(prefix='/users', tags=['Users'])

def user_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return UserService(db)

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: CreateUser, service: UserService = Depends(user_service)):
    return await service.create_user(user)

@router.get("", response_model=list[UserResponse])
async def get_all_users(service: UserService = Depends(user_service)):
    return await service.get_users()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, service: UserService = Depends(user_service)):
    return await service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UpdateUser, service: UserService = Depends(user_service)):
    return await service.update_user(user_id, user_update)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str, service: UserService = Depends(user_service)):
    await service.delete_user(user_id)

@router.get("/base/{user_id}", response_model=BaseUserResponse)
async def get_base_user(user_id: str, service: UserService = Depends(user_service)):
    return await service.get_base_user(user_id)
