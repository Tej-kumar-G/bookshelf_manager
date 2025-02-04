from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import BaseService  # Assuming you have a BaseService as in books and users

class CategoryService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['categories']  # MongoDB collection for categories

    async def create_category(self, category_data: CategoryCreate):
        category_dict = category_data.dict()
        result = await self.collection.insert_one(category_dict)
        new_category = await self.collection.find_one({'_id': result.inserted_id})
        return self._to_response(new_category, CategoryResponse)

    async def get_categories(self):
        categories = await self.collection.find().to_list(length=None)
        return [self._to_response(cat, CategoryResponse) for cat in categories]

    async def get_category(self, category_id: str):
        try:
            category = await self.collection.find_one({'_id': ObjectId(category_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return self._to_response(category, CategoryResponse)

    async def update_category(self, category_id: str, update_data: CategoryUpdate):
        try:
            result = await self.collection.update_one(
                {'_id': ObjectId(category_id)},
                {'$set': update_data.dict(exclude_unset=True)}
            )
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        updated_category = await self.collection.find_one({'_id': ObjectId(category_id)})
        return self._to_response(updated_category, CategoryResponse)

    async def delete_category(self, category_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(category_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
