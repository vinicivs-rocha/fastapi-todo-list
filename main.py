from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from handlers import item_handler

app = FastAPI()

app.include_router(item_handler.router)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
