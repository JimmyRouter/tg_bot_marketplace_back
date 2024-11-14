from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram import types, Router, F

from db_manager.manager import get_prod
from db_manager.models import Product
from .markups import cancel_kboard
from bot_core.custom_callbacks import TGProduct


my_prod_router = Router(name='my_prod_router')

@my_prod_router.callback_query(TGProduct.filter(F.view == 'prod'))
async def my_product(call: types.CallbackQuery, callback_data: TGProduct):
    k_board = InlineKeyboardBuilder()
    k_board.attach(cancel_kboard)
    product: Product = await get_prod(callback_data.shop_id, callback_data.cat_id, callback_data.id)
    k_board.button(
        text='РЕДАКТИРОВАТЬ',
        callback_data='w_start_app'

    )

    return await call.message.edit_text(
        text=f'ИНФОРМАЦИЯ О ТОВАРЕ {product["tittle"]} : \n'
             f'ЦЕНА> {product["price"]} .\n  '
             f'ОПИСАНИЕ> {product["description"]} .\n '
             f'РЕЙТИНГ> {product["rating"]["value"]} . \n'
             f'АКТИВЕН> {product["is_active"]} .',
        reply_markup=k_board.as_markup()
    )