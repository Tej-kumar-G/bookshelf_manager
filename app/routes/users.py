from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.users import UserCreate, UserUpdate, UserResponse
from app.services.users import UserService
from app.database import get_database

router = APIRouter(prefix='/users', tags=['Users'])
logger = logging.getLogger(__name__)

def user_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return UserService(db)

@router.get("/", response_model=List[UserResponse])
async def get_users(request: Request, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    return await service.get_users()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, user: UserCreate, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    return await service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(request: Request, user_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    return await service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(request: Request, user_id: str, user: UserUpdate, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    return await service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, user_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    await service.delete_user(user_id)
