from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.users import CreateUser, UserDetails, UpdateUser
from app.database import get_database
from app.services.users import UserService

user_router = APIRouter(prefix = "/users", tags = ['users'])
logger = logging.getLogger(__name__)

def user_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return UserService(db)


@user_router.post('',response_model = UserDetails)
async def create_user(request:Request, user : CreateUser, service:UserService=Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_user(user)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.get('/{user_id}',response_model = UserDetails)
async def get_user_details(request:Request, user_id:str=Path(...), service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        user = await service.get_user(user_id=user_id)
        return user
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@user_router.put("/{user_id}",response_model = UserDetails)
async def update_user(request:Request, user_id:str, user : UpdateUser, service:UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        user_update = await service.update_user(user_id=user_id,update_data=user)
        return user_update
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.delete('/{user_id}')
async def delete_user(request : Request, user_id : str, service : UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_user(user_id=user_id)
        return f"user with id {user_id} is successfully deleted"
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
