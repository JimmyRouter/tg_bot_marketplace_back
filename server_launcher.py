import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from bot_core.bot_launcher import bot_poll
from front_routes import front_router
from auth_routes import auth_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    asyncio.create_task(bot_poll(), name='poll')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(front_router)
app.include_router(auth_router)

