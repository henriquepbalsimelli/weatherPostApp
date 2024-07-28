from fastapi import FastAPI
from os.path import join, dirname
from dotenv import load_dotenv

from .routers.publications import x_publications

app = FastAPI()

app.include_router(x_publications.router)

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.get("/health")
async def read_root():
    return {"Health": 'Ok'}

