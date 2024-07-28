from fastapi.params import Query
from typing_extensions import Annotated
from fastapi import APIRouter
from app.services.x_services.x_publication_service import XPublicationService


router = APIRouter(
    prefix="/x",
)


@router.post("/publication/", tags=["publications"])
async def create_x_publication(city_name: Annotated[str, Query(min_length=3)]):
    try:
        x_publication_service = XPublicationService()
        created_publication = x_publication_service.handle_create_x_publication(city_name)
        return {"Status": f"Publicação criada com sucesso: {created_publication}"}
    except Exception as e:
        raise e