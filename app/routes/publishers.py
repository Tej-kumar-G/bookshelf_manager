from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.publishers import CreatePublisher, UpdatePublisher, PublisherResponse, BasePublisherResponse
from app.services.publishers import PublisherService
from app.database import get_database

router = APIRouter(prefix="/publishers", tags=["Publishers"])

def publisher_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return PublisherService(db)

@router.post("", response_model=PublisherResponse, status_code=201)
async def create_publisher(publisher: CreatePublisher, service: PublisherService = Depends(publisher_service)):
    return await service.create_publisher(publisher)

@router.get("", response_model=list[PublisherResponse])
async def get_publishers(service: PublisherService = Depends(publisher_service)):
    return await service.get_publishers()

@router.get("/{publisher_id}", response_model=PublisherResponse)
async def get_publisher(publisher_id: str, service: PublisherService = Depends(publisher_service)):
    return await service.get_publisher(publisher_id)

@router.put("/{publisher_id}", response_model=PublisherResponse)
async def update_publisher(publisher_id: str, publisher_update: UpdatePublisher, service: PublisherService = Depends(publisher_service)):
    return await service.update_publisher(publisher_id, publisher_update)

@router.delete("/{publisher_id}", status_code=204)
async def delete_publisher(publisher_id: str, service: PublisherService = Depends(publisher_service)):
    await service.delete_publisher(publisher_id)

@router.get("/base/{publisher_id}", response_model=BasePublisherResponse)
async def get_base_publisher(publisher_id: str, service: PublisherService = Depends(publisher_service)):
    return await service.get_base_publisher(publisher_id)
