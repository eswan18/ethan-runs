from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def hello():
    return 'Hello Ethan!'

@app.get('/hello/{name}')
async def hello_name(name: str):
    return f'Hello {name}'

@app.get('/activity/count')
async def activity_count(db: Session = Depends(get_db)):
    return db.query(models.Activity).count()
