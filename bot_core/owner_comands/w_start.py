from aiogram import types
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, )


async def w_start(msg: types.Message):
    menu_builder = InlineKeyboardBuilder()
    menu_builder.row(
        InlineKeyboardButton(text='<        ПУСК         >',
                             callback_data='w_start_app')
    )
    await msg.answer(text='<        НАЖМИТЕ ПУСК         >',
                     reply_markup=menu_builder.as_markup(resize_keyboard=True),
    )


