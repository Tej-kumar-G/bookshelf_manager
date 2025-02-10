# app/services/authors.py
from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.authors import Author
from app.schemas.authors import CreateAuthor, UpdateAuthor, AuthorResponse, BaseAuthorResponse
from app.services import BaseService
# If you have BookService for computing latest books, you can import it.
from app.services.books import BookService

class AuthorService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['authors']
        self.book_service = BookService(db)  # to fetch latest books or count published books

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def _to_response(self, doc) -> AuthorResponse:
        doc = self._replace_id(doc)
        # For latest_books, we assume BookService has a method get_latest_books(author_id)
        # and for total_published, a method count_books_by_author(author_id)
        # If not implemented yet, we can default these values.
        latest_books = await self.book_service.get_latest_books(doc['id']) if hasattr(self.book_service, 'get_latest_books') else []
        total_published = await self.book_service.count_books_by_author(doc['id']) if hasattr(self.book_service, 'count_books_by_author') else 0
        doc['latest_books'] = latest_books
        doc['total_published'] = total_published
        return AuthorResponse(**doc)

    async def create_author(self, author_data: CreateAuthor) -> AuthorResponse:
        # Check for duplicate author by name (if needed)
        existing = await self.collection.find_one({"name": author_data.name})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author with this name already exists.")
        from datetime import datetime
        author_dict = author_data.dict()
        author_dict.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        author = Author(**author_dict)
        result = await self.collection.insert_one(author.dict())
        created_author = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_author)

    async def get_author(self, author_id: str) -> AuthorResponse:
        try:
            author = await self.collection.find_one({"_id": ObjectId(author_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        return await self._to_response(author)

    async def update_author(self, author_id: str, update_data: UpdateAuthor) -> AuthorResponse:
        try:
            update_dict = update_data.dict(exclude_unset=True)
            from datetime import datetime
            update_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one({"_id": ObjectId(author_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        author = await self.collection.find_one({"_id": ObjectId(author_id)})
        return await self._to_response(author)

    async def delete_author(self, author_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(author_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid AuthorID")
    
    async def get_authors(self) -> list:
        authors = await self.collection.find().to_list(None)
        return [await self._to_response(author) for author in authors]
    
    async def get_base_author(self, author_id: str) -> BaseAuthorResponse:
        try:
            author = await self.collection.find_one({"_id": ObjectId(author_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        author = self._replace_id(author)
        return BaseAuthorResponse(**author)