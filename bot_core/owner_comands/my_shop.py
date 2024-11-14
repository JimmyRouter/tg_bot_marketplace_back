from aiogram.utils.keyboard import (InlineKeyboardBuilder)
from aiogram import types, F, Router
from .markups import cancel_kboard
from bot_core.custom_callbacks import TGShop

shop_router = Router(name='shop_router')


@shop_router.callback_query(TGShop.filter(F.view == 'my_shop'))
async def my_shop(call: types.CallbackQuery, callback_data: TGShop):
    print('calbakdata>>>>>>>>>', callback_data)
    k_board = InlineKeyboardBuilder()
    k_board.attach(cancel_kboard)
    k_board.button(
        text='ВАШИ ТОВАРЫ',
        callback_data=TGShop(
            view='cats',
            id=callback_data.id,
            tg_id=callback_data.tg_id,
            tittle=callback_data.tittle,
        )
    )
    k_board.button(
        text='ОТКРЫТЬ ПРИЛОЖЕНИЕ МАГАЗИНА',
        web_app=types.WebAppInfo(url=f'https://d7dd-117-208-42-23.ngrok-free.app/shops/{callback_data.id}'))


    k_board.adjust(1,3)
    print('kboard my shop>>>>>>>', k_board.export())
    await call.message.edit_text(
        text=f'МЕНЮ МАГАЗИНА  {callback_data.tittle}',
        reply_markup=k_board.as_markup()
    )









