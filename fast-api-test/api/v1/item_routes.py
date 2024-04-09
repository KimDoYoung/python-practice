from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from model.item_model import ItemCreate, ItemRead
from core.dependencies import db_dependency, item_service_dependency, get_item_service
from service.item_service import ItemService

router = APIRouter()

@router.post("/items/", response_model=ItemRead)
async def create_item(item: ItemCreate, background_tasks: BackgroundTasks, db: db_dependency, service: item_service_dependency):
    created_item = await service.create(item, db)
    background_tasks.add_task(log_operation, created_item.id)
    return created_item

@router.get("/items/", response_model=list[ItemRead])
async def read_items(db: db_dependency, service: item_service_dependency):
    return await service.get_all(db)

@router.get("/items/{id}", response_model=ItemRead)
async def read_item(id: int, db: db_dependency, service: item_service_dependency):
    item = await service.get(id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def log_operation(id: int):
    print(f"Item with id {id} was created")
