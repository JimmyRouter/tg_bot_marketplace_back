from aiogram import types
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, )


async def start(msg: types.Message):
    user_id = msg.from_user.id
    menu_builder = InlineKeyboardBuilder()
    menu_builder.row(
        InlineKeyboardButton(text='<        ПУСК         >',
                             callback_data='start_app')
    )
    menu_builder.adjust(1)
    await msg.answer(text='<        НАЖМИТЕ ПУСК         >',
                     reply_markup=menu_builder.as_markup(resize_keyboard=True),
    )


