from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.users import User
from app.schemas.users import CreateUser, UpdateUser, UserResponse, BaseUserResponse
from app.services import BaseService
from app.services.books import BookService
from app.services.reviews import ReviewService


class UserService(BaseService):
    
    def __init__(self, db:AsyncIOMotorDatabase):
        super().__init__(db)
        self.db = db
        self.collection = db['users']

    @property
    def book_service(self):
        return BookService(self.db)
    
    @property
    def review_service(self):
        return ReviewService(self.db)

    def _replace_id(self, doc):
        doc['id'] = str(doc.pop('_id'))
        return doc

    async def _to_response(self, doc):
        doc = self._replace_id(doc)
        # doc['latest_books'] = await self.book_service.get_latest_books(doc['id'])
        doc['total_reviews'] = await self.review_service.get_total_reviews(doc['id'])
        return UserResponse(**doc)
    
    async def create_user(self, user_data:CreateUser):
        print(user_data)
        user = User(**user_data.dict())
        result = await self.collection.insert_one(user.dict())
        user = await self.collection.find_one({'_id':result.inserted_id})
        return await self._to_response(user)
    
    async def get_user(self, user_id: str):
        try:
            user = await self.collection.find_one({'_id': ObjectId(user_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return await self._to_response(user)
    
    async def update_user(self, user_id: str, update_data: UpdateUser):
        try:
            result = await self.collection.update_one({'_id': ObjectId(user_id)},
                                                      {'$set': update_data.dict(exclude_unset=True)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        return await self._to_response(user)
    
    async def delete_user(self, user_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(user_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UserID")
        
    async def get_users(self):
        users = await self.collection.find().to_list(None)
        return [self._to_response(user) for user in users]
    
    async def get_base_user(self, user_id: str):
        try:
            user = await self.collection.find_one({'_id': ObjectId(user_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = self._replace_id(user)
        return BaseUserResponse(**user)
