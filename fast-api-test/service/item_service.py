from sqlalchemy.future import select as async_select
from model.item_model import Item, ItemCreate
from sqlmodel import Session

class ItemService:
    async def create(self, item: ItemCreate, db: Session) -> Item:
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    async def get(self, id: int, db: Session) -> Item:
        async with db as session:
            statement = async_select(Item).where(Item.id == id)
            result = await session.execute(statement)
            item = result.scalars().first()
            return item
            
    async def get_all(self, db: Session):
        async with db as session:
            statement = async_select(Item)
            result = await session.execute(statement)
            items = result.scalars().all()
            return items
