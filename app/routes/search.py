from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.services.books import BookService
from app.services.authors import AuthorService
from app.services.categories import CategoryService
from app.services.reviews import ReviewService
from app.services.users import UserService

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/books")
async def search_books(
    q: str = Query(..., description="Search query for books"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Search for books by name or description
    cursor = db["books"].find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    })
    books = await cursor.to_list(length=100)
    service = BookService(db)
    results = []
    for book in books:
        results.append(await service._to_response(book))
    return {"results": results}

@router.get("/authors")
async def search_authors(
    q: str = Query(..., description="Search query for authors"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Search authors by name
    cursor = db["authors"].find({
        "name": {"$regex": q, "$options": "i"}
    })
    authors = await cursor.to_list(length=100)
    service = AuthorService(db)
    results = []
    for author in authors:
        results.append(await service._to_response(author))
    return {"results": results}

@router.get("/categories")
async def search_categories(
    q: str = Query(..., description="Search query for categories"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Search categories by name or description
    cursor = db["categories"].find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    })
    categories = await cursor.to_list(length=100)
    service = CategoryService(db)
    results = []
    for category in categories:
        results.append(await service._to_response(category))
    return {"results": results}

@router.get("/reviews")
async def search_reviews(
    q: str = Query(..., description="Search query for reviews"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Search reviews by content
    cursor = db["reviews"].find({
        "content": {"$regex": q, "$options": "i"}
    })
    reviews = await cursor.to_list(length=100)
    service = ReviewService(db)
    results = []
    for review in reviews:
        results.append(await service._to_response(review))
    return {"results": results}

@router.get("/users")
async def search_users(
    q: str = Query(..., description="Search query for users"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Search users by name, email, or phone_number
    cursor = db["users"].find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
            {"phone_number": {"$regex": q, "$options": "i"}}
        ]
    })
    users = await cursor.to_list(length=100)
    service = UserService(db)
    results = []
    for user in users:
        results.append(await service._to_response(user))
    return {"results": results}
