from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
