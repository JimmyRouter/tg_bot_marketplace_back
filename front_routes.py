from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
import db_manager

front_router = APIRouter()


@front_router.get("/")
async def read_root():
    return {"Hello": "World"}


@front_router.get("/shops/{shop_id}",)
async def get_shop(shop_id, request: Request):
    shop = await db_manager.getshop(shop_id)
    return shop


@front_router.get("/images/{shop_id}/{img_name}")
async def get_img(shop_id, img_name):
    return FileResponse(f'bot_core/files/{shop_id}/photos/{img_name}')


