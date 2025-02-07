# app/services/users.py
from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.users import User
from app.schemas.users import CreateUser, UpdateUser, UserResponse, BaseUserResponse
from app.services import BaseService
from app.services.books import BookService  # if needed
from app.services.reviews import ReviewService  # if needed

class UserService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
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
        # For demonstration, if review_service is not implemented, default to 0
        doc['total_reviews'] = await self.review_service.get_total_reviews(doc['id']) if hasattr(self.review_service, 'get_total_reviews') else 0
        return UserResponse(**doc)
    
    async def create_user(self, user_data: CreateUser):
        existing = await self.collection.find_one({"email": user_data.email})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
        user_dict = user_data.dict()
        from datetime import datetime
        user_dict.update({
            "total_reviews": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        user = User(**user_dict)
        result = await self.collection.insert_one(user.dict())
        user = await self.collection.find_one({'_id': result.inserted_id})
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
            update_dict = update_data.dict(exclude_unset=True)
            from datetime import datetime
            update_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        return await self._to_response(user)
    
    async def delete_user(self, user_id: str) -> None:
        try:
            result = await self.collection.delete_one({'_id': ObjectId(user_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UserID")
        
    async def get_users(self):
        users = await self.collection.find().to_list(None)
        return [await self._to_response(user) for user in users]
    
    async def get_base_user(self, user_id: str):
        try:
            user = await self.collection.find_one({'_id': ObjectId(user_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = self._replace_id(user)
        return BaseUserResponse(**user)
