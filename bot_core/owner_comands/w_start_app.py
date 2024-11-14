from aiogram import types

import db_manager.manager as db_manager
from .markups import index_markup

async def w_start_app(call: types.CallbackQuery):
    await db_manager.checkin(call, 'owner')
    # await db_manager.extract_data(call)


    await call.message.edit_text(
        text='<   ГЛАВНОЕ  МЕНЮ   >',
        reply_markup=index_markup.as_markup(),
    )