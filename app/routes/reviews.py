from fastapi import APIRouter, Depends, HTTPException, Request, status, Query, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.reviews import WriteReview, ReviewResponse, UpdatReview
from app.database import get_database
from app.services.reviews import ReviewService


review_router = APIRouter(prefix = "/reviews", tags = ['reviews'])
logger = logging.getLogger(__name__)

def review_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return ReviewService(db)

@review_router.post('',response_model = ReviewResponse)
async def write_review(request:Request, review : WriteReview, service:ReviewService=Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.write_review(review)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

@review_router.get('/{book_id}', response_model=List[ReviewResponse])
async def get_all_reviews(
    request: Request,
    book_id: str = Path(...),  
    service: ReviewService = Depends(review_service)
):
    logger.info(f"Request path: {request.url.path}")
    try:
        reviews = await service.get_reviews(book_id=book_id)
        return reviews
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@review_router.put("/{review_id}",response_model = ReviewResponse)
async def update_review(request:Request, review_id : str, update_review : UpdatReview, service:ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        review_update = await service.update_review(review_id=review_id,update_review=update_review)
        return review_update
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@review_router.delete("/{review_id}")
async def delete_review(request:Request,review_id:str,service:ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        result = await service.delete_review(review_id=review_id)
        return result
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


