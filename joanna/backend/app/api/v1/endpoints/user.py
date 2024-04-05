from fastapi import APIRouter


router = APIRouter()

@router.get("/user/{id}")
def read_user(id: str):
    return {"id": id}
