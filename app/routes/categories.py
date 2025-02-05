from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.categories import CreateCategory,CategoryResponse,UpdateCategory
from app.database import get_database
from app.services.categories import CategoryService


category_router = APIRouter(prefix= "/category",tags = ['categories'])
logger = logging.getLogger(__name__)

def category_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return CategoryService(db)

@category_router.post('',response_model = CategoryResponse)
async def create_category(request:Request, category_data:CreateCategory, service : CategoryService=Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_category(category_data=category_data)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@category_router.get('',response_model = List[CategoryResponse])
async def get_all_categories(request:Request, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        categories = await service.get_categories()
        return categories
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@category_router.put('/{category_id}',response_model = CategoryResponse)
async def update_category(request:Request, category_id:str, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        update = await service.update_category(category_id=category_id)
        return update
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@category_router.delete('/{category_id}')
async def delete_user(request : Request, category_id : str, service : CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_category(category_id=category_id)
        return f"category with id {category_id} is successfully deleted"
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")