from bson.objectid import ObjectId
from fastapi import HTTPException, status
from app.models.authors import Author
from app.schemas.authors import AuthorCreate, AuthorResponse, AuthorUpdate
from app.services import BaseService
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class AuthorService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['authors']

    async def create_author(self, author_data: AuthorCreate):
        author = Author(**author_data.dict())
        # Insert after converting birth_date to ISO string
        result = await self.collection.insert_one(author.dict())
        author = await self.collection.find_one({'_id': result.inserted_id})
        return self._to_response(author, AuthorResponse)

    async def get_author(self, author_id: str):
        author = await self.collection.find_one({'_id': ObjectId(author_id)})
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        return self._to_response(author, AuthorResponse)

    async def update_author(self, author_id: str, update_data: AuthorUpdate):
        result = await self.collection.update_one(
            {'_id': ObjectId(author_id)},
            {'$set': update_data.dict(exclude_unset=True)}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        author = await self.collection.find_one({'_id': ObjectId(author_id)})
        return self._to_response(author, AuthorResponse)

    async def delete_author(self, author_id: str):
        result = await self.collection.delete_one({'_id': ObjectId(author_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    async def get_authors(self):
        authors = await self.collection.find().to_list(None)
        return [self._to_response(author, AuthorResponse) for author in authors]
