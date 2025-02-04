from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.reviews import Review
from app.schemas.reviews import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services import BaseService

class ReviewService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['reviews']

    async def create_review(self, book_id: str, review_data: ReviewCreate):
        review = Review(book_id=book_id, **review_data.dict())
        result = await self.collection.insert_one(review.dict())
        saved_review = await self.collection.find_one({'_id': result.inserted_id})
        return self._to_response(saved_review, ReviewResponse)

    async def get_reviews(self, book_id: str):
        reviews = await self.collection.find({'book_id': book_id}).to_list(None)
        return [self._to_response(review, ReviewResponse) for review in reviews]

    async def update_review(self, book_id: str, review_id: str, update_data: ReviewUpdate):
        try:
            result = await self.collection.update_one(
                {'_id': ObjectId(review_id), 'book_id': book_id},
                {'$set': update_data.dict(exclude_unset=True)}
            )
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        
        updated_review = await self.collection.find_one({'_id': ObjectId(review_id)})
        return self._to_response(updated_review, ReviewResponse)

    async def delete_review(self, book_id: str, review_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(review_id), 'book_id': book_id})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
