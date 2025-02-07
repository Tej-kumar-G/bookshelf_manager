from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.bookstore import Bookstore
from app.schemas.bookstores import CreateBookstore, UpdateBookstore, BookstoreResponse, BaseBookstoreResponse
from app.services import BaseService
from datetime import datetime

class BookstoreService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['bookstores']
        self.book_collection = db['books']

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def _to_response(self, doc) -> BookstoreResponse:
        doc = self._replace_id(doc)
        book_ids = doc.get("book_ids", [])
        books = []
        for book_id in book_ids:
            try:
                book = await self.book_collection.find_one({"_id": ObjectId(book_id)})
                if book:
                    books.append({"id": str(book["_id"]), "name": book.get("name")})
            except Exception:
                continue
        doc["books"] = books
        return BookstoreResponse(**doc)

    async def create_bookstore(self, bookstore_data: CreateBookstore) -> BookstoreResponse:
        existing = await self.collection.find_one({"name": bookstore_data.name})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bookstore with this name already exists.")
        bookstore_dict = bookstore_data.dict()
        bookstore_dict.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "book_ids": []
        })
        bookstore = Bookstore(**bookstore_dict)
        result = await self.collection.insert_one(bookstore.dict())
        created_bookstore = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_bookstore)

    async def get_bookstore(self, bookstore_id: str) -> BookstoreResponse:
        try:
            bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not bookstore:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")
        return await self._to_response(bookstore)

    async def update_bookstore(self, bookstore_id: str, update_data: UpdateBookstore) -> BookstoreResponse:
        try:
            update_dict = update_data.dict(exclude_unset=True)
            update_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one({"_id": ObjectId(bookstore_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")
        updated_bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        return await self._to_response(updated_bookstore)

    async def delete_bookstore(self, bookstore_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(bookstore_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")

    async def get_bookstores(self) -> list:
        bookstores = await self.collection.find().to_list(None)
        return [await self._to_response(bookstore) for bookstore in bookstores]

    async def add_book_to_bookstore(self, bookstore_id: str, book_id: str) -> BookstoreResponse:
        bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        if not bookstore:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")
        await self.collection.update_one({"_id": ObjectId(bookstore_id)}, {"$addToSet": {"book_ids": book_id}})
        updated_bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        return await self._to_response(updated_bookstore)

    async def remove_book_from_bookstore(self, bookstore_id: str, book_id: str) -> BookstoreResponse:
        bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        if not bookstore:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")
        await self.collection.update_one({"_id": ObjectId(bookstore_id)}, {"$pull": {"book_ids": book_id}})
        updated_bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        return await self._to_response(updated_bookstore)

    async def get_base_bookstore(self, bookstore_id: str) -> BaseBookstoreResponse:
        try:
            bookstore = await self.collection.find_one({"_id": ObjectId(bookstore_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not bookstore:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookstore not found")
        bookstore = self._replace_id(bookstore)
        return BaseBookstoreResponse(**{"id": bookstore["id"], "name": bookstore.get("name")})
