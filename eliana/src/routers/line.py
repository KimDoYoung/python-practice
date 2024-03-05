from fastapi import APIRouter
#from models import Item

router = APIRouter()

@router.get("/chart/line")
async def read_item():
    return {"item_id": 111}

