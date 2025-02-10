from fastapi import APIRouter, Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from app.schemas.bookstores import CreateBookstore, UpdateBookstore, BookstoreResponse, BaseBookstoreResponse
from app.services.bookstores import BookstoreService
from app.database import get_database

bookstore_router = APIRouter(prefix="/bookstores", tags=["Bookstores"])

def bookstore_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return BookstoreService(db)

@bookstore_router.post("", response_model=BookstoreResponse, status_code=201)
async def create_bookstore(request: Request, bookstore: CreateBookstore, service: BookstoreService = Depends(bookstore_service)):
    return await service.create_bookstore(bookstore)

@bookstore_router.get("", response_model=List[BookstoreResponse])
async def get_bookstores(request: Request, service: BookstoreService = Depends(bookstore_service)):
    return await service.get_bookstores()

@bookstore_router.get("/{bookstore_id}", response_model=BookstoreResponse)
async def get_bookstore(request: Request, bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
    return await service.get_bookstore(bookstore_id)

@bookstore_router.put("/{bookstore_id}", response_model=BookstoreResponse)
async def update_bookstore(request: Request, bookstore_id: str, bookstore_update: UpdateBookstore, service: BookstoreService = Depends(bookstore_service)):
    return await service.update_bookstore(bookstore_id, bookstore_update)

@bookstore_router.delete("/{bookstore_id}", status_code=204)
async def delete_bookstore(request: Request, bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
    await service.delete_bookstore(bookstore_id)

@bookstore_router.post("/{bookstore_id}/books/{book_id}", response_model=BookstoreResponse)
async def add_book_to_bookstore(request: Request, bookstore_id: str, book_id: str, service: BookstoreService = Depends(bookstore_service)):
    return await service.add_book_to_bookstore(bookstore_id, book_id)

@bookstore_router.delete("/{bookstore_id}/books/{book_id}", response_model=BookstoreResponse)
async def remove_book_from_bookstore(request: Request, bookstore_id: str, book_id: str, service: BookstoreService = Depends(bookstore_service)):
    return await service.remove_book_from_bookstore(bookstore_id, book_id)

@bookstore_router.get("/base/{bookstore_id}", response_model=BaseBookstoreResponse)
async def get_base_bookstore(bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
    return await service.get_base_bookstore(bookstore_id)