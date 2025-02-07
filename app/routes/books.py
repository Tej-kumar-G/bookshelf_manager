# app/routes/books.py
from fastapi import APIRouter, Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from app.schemas.books import CreateBook, UpdateBook, BookResponse, BaseBookResponse
from app.services.books import BookService
from app.database import get_database

router = APIRouter(prefix="/books", tags=["Books"])

def book_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return BookService(db)

@router.post("", response_model=BookResponse, status_code=201)
async def create_book(request: Request, book: CreateBook, service: BookService = Depends(book_service)):
    return await service.create_book(book)

@router.get("", response_model=List[BookResponse])
async def get_books(request: Request, service: BookService = Depends(book_service)):
    return await service.get_books()

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(request: Request, book_id: str, service: BookService = Depends(book_service)):
    return await service.get_book(book_id)

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(request: Request, book_id: str, book_update: UpdateBook, service: BookService = Depends(book_service)):
    return await service.update_book(book_id, book_update)

@router.delete("/{book_id}", status_code=204)
async def delete_book(request: Request, book_id: str, service: BookService = Depends(book_service)):
    await service.delete_book(book_id)

@router.get("/base/{book_id}", response_model=BaseBookResponse)
async def get_base_book(book_id: str, service: BookService = Depends(book_service)):
    return await service.get_base_book(book_id)
