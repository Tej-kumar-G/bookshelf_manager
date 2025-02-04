from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.authors import AuthorCreate, AuthorUpdate, AuthorResponse
from app.services.authors import AuthorService
from app.database import get_database

router = APIRouter(prefix='/authors', tags=['Authors'])
logger = logging.getLogger(__name__)

def author_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return AuthorService(db)

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(request: Request, author: AuthorCreate, service: AuthorService = Depends(author_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_author(author)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/", response_model=List[AuthorResponse])
async def get_authors(request: Request, service: AuthorService = Depends(author_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_authors()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(request: Request, author_id: str, service: AuthorService = Depends(author_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_author(author_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(request: Request, author_id: str, author: AuthorUpdate, service: AuthorService = Depends(author_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_author(author_id, author)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(request: Request, author_id: str, service: AuthorService = Depends(author_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_author(author_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
