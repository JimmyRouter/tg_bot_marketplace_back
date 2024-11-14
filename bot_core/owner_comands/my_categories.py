from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram import types, F, Router
from .markups import cancel_kboard
from bot_core.custom_callbacks import TGShop, TGCategory
from db_manager.manager import get_shop_categories


categories_router = Router(name='cats_router')


@categories_router.callback_query(TGShop.filter(F.view == 'cats'))
async def my_categories(call: types.CallbackQuery, callback_data: TGShop):
    print('my categoris calbdata>>>', callback_data.pack())
    categories = await get_shop_categories(shop_id=callback_data.id)
    k_board = InlineKeyboardBuilder()
    k_board.attach(cancel_kboard)
    k_board.button(text='ДОБАВИТЬ КАТЕГОРИЮ ТОВАРОВ',
                   callback_data=TGCategory(
                       view='add_cat',
                       shop_id=callback_data.id,
                   )
                   )

    for cat in categories:
        k_board.button(text=cat['tittle'],
                       callback_data=TGCategory(
                           view='cat',
                           shop_id=callback_data.id,
                           id=cat['_id'],
                           tittle=cat['tittle'],
                                                )
                       )

    k_board.adjust(1,1,1)
    print('my_cats kboard>>>>>',k_board.export())
    await call.message.edit_text(text='ВАШИ КАТЕГОРИИ ТОВАРОВ',
                                 reply_markup=k_board.as_markup()
                                 )


