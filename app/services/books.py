# app/services/books.py
from bson.objectid import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from app.models.books import Book
from app.schemas.books import CreateBook, UpdateBook, BookResponse, BaseBookResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services import BaseService

class BookService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['books']
        self.review_collection = db['reviews']

    async def create_book(self, book_data: CreateBook) -> BookResponse:
        # Check for duplicate book name
        existing = await self.collection.find_one({"name": book_data.name})
        if existing:
            raise HTTPException(status_code=409, detail="Book with this name already exists.")
        from datetime import datetime
        book_dict = book_data.dict()
        book_dict.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        book = Book(**book_dict)
        result = await self.collection.insert_one(book.dict())
        created_book = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_book)

    async def get_book(self, book_id: str) -> BookResponse:
        try:
            book = await self.collection.find_one({"_id": ObjectId(book_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return await self._to_response(book)

    async def update_book(self, book_id: str, update_data: UpdateBook) -> BookResponse:
        try:
            update_dict = update_data.dict(exclude_unset=True)
            from datetime import datetime
            update_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        updated_book = await self.collection.find_one({"_id": ObjectId(book_id)})
        return await self._to_response(updated_book)

    async def delete_book(self, book_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(book_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    async def get_books(self) -> list:
        books = await self.collection.find().to_list(None)
        return [await self._to_response(book) for book in books]

    async def _to_response(self, book: dict) -> BookResponse:
        # Fetch related data dynamically
        try:
            author = await self.db["authors"].find_one({"_id": ObjectId(book.get("author_id"))})
        except Exception:
            author = None
        try:
            category = await self.db["categories"].find_one({"_id": ObjectId(book.get("category_id"))})
        except Exception:
            category = None
        publisher = None
        if book.get("publisher_id"):
            try:
                publisher = await self.db["publishers"].find_one({"_id": ObjectId(book.get("publisher_id"))})
            except Exception:
                publisher = None
        is_published = True if publisher else False

        # Aggregate reviews: match on the string value of the book's _id
        pipeline = [
            {"$match": {"book_id": str(book.get("_id"))}},
            {"$group": {"_id": "$book_id", "average": {"$avg": "$rating"}, "count": {"$sum": 1}}}
        ]
        agg = await self.review_collection.aggregate(pipeline).to_list(length=1)
        average_rating = agg[0]["average"] if agg else None
        total_reviews = agg[0]["count"] if agg else 0

        # Replace _id with id
        book["id"] = str(book["_id"])
        del book["_id"]

        return BookResponse(
            id=book["id"],
            name=book.get("name"),
            description=book.get("description"),
            author={"id": book.get("author_id"), "name": author.get("name") if author else "Unknown"},
            category={"id": book.get("category_id"), "name": category.get("name") if category else "Unknown"},
            publisher={"id": book.get("publisher_id"), "name": publisher.get("name")} if publisher else None,
            is_published=is_published,
            average_rating=average_rating,
            total_reviews=total_reviews,
            created_at=book.get("created_at"),
            updated_at=book.get("updated_at")
        )

    async def get_base_book(self, book_id: str) -> BaseBookResponse:
        try:
            book = await self.collection.find_one({"_id": ObjectId(book_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        book["id"] = str(book["_id"])
        del book["_id"]
        return BaseBookResponse(**{"id": book["id"], "name": book.get("name")})