# app/routes/reviews.py
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.reviews import CreateReview, UpdateReview, ReviewResponse, BaseReviewResponse
from app.services.reviews import ReviewService
from app.database import get_database

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def review_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return ReviewService(db)

@router.post("", response_model=ReviewResponse, status_code=201)
async def create_review(review: CreateReview, service: ReviewService = Depends(review_service)):
    return await service.create_review(review)

@router.get("", response_model=list[ReviewResponse])
async def get_all_reviews(service: ReviewService = Depends(review_service)):
    return await service.get_reviews()

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: str, service: ReviewService = Depends(review_service)):
    return await service.get_review(review_id)

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: str, review_update: UpdateReview, service: ReviewService = Depends(review_service)):
    return await service.update_review(review_id, review_update)

@router.delete("/{review_id}", status_code=204)
async def delete_review(review_id: str, service: ReviewService = Depends(review_service)):
    await service.delete_review(review_id)

@router.get("/base/{review_id}", response_model=BaseReviewResponse)
async def get_base_review(review_id: str, service: ReviewService = Depends(review_service)):
    return await service.get_base_review(review_id)
