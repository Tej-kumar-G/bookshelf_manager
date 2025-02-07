# app/routes/authors.py
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.authors import CreateAuthor, UpdateAuthor, AuthorResponse, BaseAuthorResponse
from app.services.authors import AuthorService
from app.database import get_database

router = APIRouter(prefix='/authors', tags=['Authors'])

def author_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return AuthorService(db)

@router.post("", response_model=AuthorResponse, status_code=201)
async def create_author(author: CreateAuthor, service: AuthorService = Depends(author_service)):
    return await service.create_author(author)

@router.get("", response_model=list[AuthorResponse])
async def get_all_authors(service: AuthorService = Depends(author_service)):
    return await service.get_authors()

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: str, service: AuthorService = Depends(author_service)):
    return await service.get_author(author_id)

@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(author_id: str, author_update: UpdateAuthor, service: AuthorService = Depends(author_service)):
    return await service.update_author(author_id, author_update)

@router.delete("/{author_id}", status_code=204)
async def delete_author(author_id: str, service: AuthorService = Depends(author_service)):
    await service.delete_author(author_id)

@router.get("/base/{author_id}", response_model=BaseAuthorResponse)
async def get_base_author(author_id: str, service: AuthorService = Depends(author_service)):
    return await service.get_base_author(author_id)
