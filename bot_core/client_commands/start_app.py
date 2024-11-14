from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import db_manager.manager as db_manager
import constants



async def start_app(call: types.CallbackQuery):
    await db_manager.checkin(call)
    shop_id = call.message.from_user.id
    # await db_manager.extract_data(call)
    index_page_builder = InlineKeyboardBuilder()
    index_page_builder.button(
        text='✅       МОИ ЗАКАЗЫ       ', callback_data='my_orders',
    )
    index_page_builder.button(
        text='✅       В МАГАЗИН     ', web_app=WebAppInfo(url=f'{constants.TG_WEBAPP_URI}/{shop_id}')
                            )
    index_page_builder.button(
        text='✅       МОИ НАСТРОЙКИ     ', callback_data='my_set'
    )

    index_page_builder.adjust(1,1,1)

    await call.message.edit_text(
        text='<        МЕНЮ        >',
        reply_markup=index_page_builder.as_markup(resize_keyboard=True)
    )