from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def my_orders(call: types.CallbackQuery):
    user_id = call.from_user.id
    shop_id = call.message.from_user.id
    menu_builder = InlineKeyboardBuilder()
    menu_builder.button(
        text='to call help', callback_data='call_help'
    )
    menu_builder.button(
        text='to start', callback_data='start'),

    await call.message.edit_text(text=':on:',
                      reply_markup=menu_builder.as_markup(resize_keyboard=True)
                      # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())
                      )