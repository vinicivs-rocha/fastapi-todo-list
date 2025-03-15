from fastapi import FastAPI

from handlers import item_handler

app = FastAPI()

app.include_router(item_handler.router)
