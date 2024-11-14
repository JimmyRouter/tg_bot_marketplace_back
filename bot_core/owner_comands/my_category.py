from typing import List
from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram import types, F, Router
from db_manager.models import Product
from .markups import cancel_kboard
from bot_core.custom_callbacks import TGCategory, TGProduct
from db_manager.manager import get_products


my_cat_router = Router(name='my_cat_router')

@my_cat_router.callback_query(TGCategory.filter(F.view == 'cat'))
async def my_category(call: types.CallbackQuery, callback_data: TGCategory):
    products: List[Product] = await get_products(callback_data.shop_id, callback_data.id)
    k_board = InlineKeyboardBuilder()
    k_board.attach(cancel_kboard)
    k_board.button(
        text='ДОБАВИТЬ ТОВАР',
        callback_data=TGProduct(
            view='add_prod',
            shop_id=callback_data.shop_id,
            cat_id=callback_data.id,
        )
    )

    if products:
        for product in products:
            k_board.button(
                text=product['tittle'],
                callback_data=TGProduct(
                    view='prod',
                    shop_id=callback_data.shop_id,
                    cat_id=callback_data.id,
                    id=product['_id'],
                )
            )


    print('my_prodsucts got>>>', products)
    k_board.adjust(1, 1, 1)
    await call.message.edit_text(text=f'ТОВАРЫ КАТЕГОРИИ "{callback_data.tittle}"',
                                 reply_markup=k_board.as_markup())

