from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.reviews import ReviewService
from app.database import get_database

router = APIRouter(prefix='/books/{book_id}/reviews', tags=['Reviews'])
logger = logging.getLogger(__name__)

def review_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return ReviewService(db)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(request: Request, book_id: str, review: ReviewCreate, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_review(book_id, review)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(request: Request, book_id: str, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_reviews(book_id)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(request: Request, book_id: str, review_id: str, review: ReviewUpdate, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_review(book_id, review_id, review)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(request: Request, book_id: str, review_id: str, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_review(book_id, review_id)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
