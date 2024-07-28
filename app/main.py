from fastapi import FastAPI
from os.path import join, dirname
from dotenv import load_dotenv

from .routers.publications import x_publications

app = FastAPI()

app.include_router(x_publications.router)

dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')
load_dotenv(dotenv_path)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.get("/health")
async def read_root():
    return {"Health": 'Ok'}

