from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .markups import cancel_kboard
from bot_core.custom_callbacks import TGShop
from db_manager.manager import get_owner_shops


async def my_shops(call: types.CallbackQuery):
    user_id = call.from_user.id
    k_board = InlineKeyboardBuilder()
    shops = await get_owner_shops(user_id)
    print('shops>>', shops)
    k_board.button(
        text='ДОБАВИТЬ МАГАЗИН',
        callback_data='add_shop'
    )
    k_board.attach(cancel_kboard)
    for shop in shops:
        k_board.button(
            text=f'{shop["tittle"]}    ✅',
            callback_data=TGShop(view='my_shop',
                                 id=shop["_id"],
                                 tg_id=shop['tg_id'],
                                 tittle=shop["tittle"],
                                 is_running=shop['is_running'],
                                 ),

            )

    k_board.adjust(1,1,1)
    print('kboard myshpSS>>>>>>>><<<<<<<', k_board.export())
    await call.message.edit_text(text='ВАШИ МАГАЗИНЫ',
                                 reply_markup=k_board.as_markup(resize_keyboard=True)
                                 )
