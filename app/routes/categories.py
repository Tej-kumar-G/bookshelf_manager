from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.categories import CreateCategory, UpdateCategory, CategoryResponse, BaseCategoryResponse
from app.services.categories import CategoryService
from app.database import get_database

category_router = APIRouter(prefix="/categories", tags=["Categories"])

def category_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return CategoryService(db)

@category_router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(category: CreateCategory, service: CategoryService = Depends(category_service)):
    return await service.create_category(category)

@category_router.get("", response_model=list[CategoryResponse])
async def get_all_categories(service: CategoryService = Depends(category_service)):
    return await service.get_categories()

@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str, service: CategoryService = Depends(category_service)):
    return await service.get_category(category_id)

@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: str, category_update: UpdateCategory, service: CategoryService = Depends(category_service)):
    return await service.update_category(category_id, category_update)

@category_router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str, service: CategoryService = Depends(category_service)):
    await service.delete_category(category_id)

@category_router.get("/base/{category_id}", response_model=BaseCategoryResponse)
async def get_base_category(category_id: str, service: CategoryService = Depends(category_service)):
    return await service.get_base_category(category_id)