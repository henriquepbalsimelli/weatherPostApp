from fastapi import FastAPI

from .routers.publications import x_publications

app = FastAPI()

app.include_router(x_publications.router)


@app.get("/health")
async def read_root():
    return {"Health": 'Ok'}

