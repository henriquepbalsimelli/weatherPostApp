from fastapi import APIRouter

router = APIRouter(
    prefix="/x",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/users/", tags=["users"])
async def read_users():
    return fake_items_db

@router.post("/publication", tags=["publications"])
async def create_x_publication():
    return {'status': 'created'}