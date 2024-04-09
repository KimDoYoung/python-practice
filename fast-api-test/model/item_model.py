from sqlmodel import Field, SQLModel

class ItemBase(SQLModel):
    name: str
    description: str = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)

class ItemRead(ItemBase):
    id: int
