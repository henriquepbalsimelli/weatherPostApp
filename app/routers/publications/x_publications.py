from fastapi.params import Query
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException
from app.services.x_services.x_publication_service import XPublicationService

from tweepy.errors import HTTPException as TweepyHTTPException

router = APIRouter(
    prefix="/x",
)


@router.post("/publication/", tags=["publications"])
async def create_x_publication(city_name: Annotated[str, Query(min_length=3)]):
    try:
        x_publication_service = XPublicationService()
        created_publication = x_publication_service.handle_create_x_publication(city_name)
        return {"Status": f"Publicação criada com sucesso: {created_publication}"}
    except TweepyHTTPException as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.api_messages
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Houve um problema inesperado"
        )