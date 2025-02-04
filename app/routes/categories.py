from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.categories import CategoryService
from app.database import get_database

router = APIRouter(prefix='/categories', tags=['Categories'])
logger = logging.getLogger(__name__)

def category_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return CategoryService(db)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(request: Request, category: CategoryCreate, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_category(category)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(request: Request, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_categories()
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(request: Request, category_id: str, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_category(category_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(request: Request, category_id: str, category: CategoryUpdate, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_category(category_id, category)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(request: Request, category_id: str, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_category(category_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
