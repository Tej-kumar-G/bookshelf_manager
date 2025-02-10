# app/services/reviews.py
from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.reviews import Review
from app.schemas.reviews import CreateReview, UpdateReview, ReviewResponse, BaseReviewResponse
from app.services import BaseService

class ReviewService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['reviews']

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def _to_response(self, doc) -> ReviewResponse:
        doc = self._replace_id(doc)
        # Fetch user name and book title from respective collections
        try:
            user = await self.db['users'].find_one({'_id': ObjectId(doc.get("created_by_id"))})
            book = await self.db['books'].find_one({'_id': ObjectId(doc.get("book_id"))})
        except Exception:
            user = None
            book = None
        doc['created_by'] = {
            "id": doc.get("created_by_id"),
            "name": user.get("name") if user else "Unknown"
        }
        doc['book'] = {
            "id": doc.get("book_id"),
            "name": book.get("name") if book else "Unknown"
        }
        return ReviewResponse(**doc)

    async def create_review(self, review_data: CreateReview) -> ReviewResponse:
        from datetime import datetime
        review_dict = review_data.dict()
        review_dict.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        review = Review(**review_dict)
        result = await self.collection.insert_one(review.dict())
        created_review = await self.collection.find_one({'_id': result.inserted_id})
        return await self._to_response(created_review)

    async def get_review(self, review_id: str) -> ReviewResponse:
        try:
            review = await self.collection.find_one({'_id': ObjectId(review_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return await self._to_response(review)

    async def update_review(self, review_id: str, update_data: UpdateReview) -> ReviewResponse:
        try:
            update_dict = update_data.dict(exclude_unset=True)
            from datetime import datetime
            update_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one({'_id': ObjectId(review_id)}, {'$set': update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        review = await self.collection.find_one({'_id': ObjectId(review_id)})
        return await self._to_response(review)

    async def delete_review(self, review_id: str) -> None:
        try:
            result = await self.collection.delete_one({'_id': ObjectId(review_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    async def get_reviews(self) -> list:
        reviews = await self.collection.find().to_list(None)
        return [await self._to_response(review) for review in reviews]

    async def get_base_review(self, review_id: str) -> BaseReviewResponse:
        try:
            review = await self.collection.find_one({'_id': ObjectId(review_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        review = self._replace_id(review)
        return BaseReviewResponse(**review)