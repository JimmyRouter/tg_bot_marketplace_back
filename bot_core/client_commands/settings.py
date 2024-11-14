from aiogram import types
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardMarkup, ReplyKeyboardMarkup,
                                    InlineKeyboardButton, KeyboardButton,
                                    KeyboardButtonPollType,
                                    )

async def my_set(msg:types.Message):
    menu_builder = InlineKeyboardBuilder()
    menu_builder.button(
        text='to call help', callback_data='call_help'
    )
    menu_builder.button(
        text='to start', callback_data='start'),


    await msg.answer(text='my set',
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
        # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())
    )

async def settings(call:types.CallbackQuery):
    settings_builder = InlineKeyboardBuilder()
    settings_builder.button(
        text='help',
        callback_data='call_help'
    )

    await call.message.edit_text(text='settings>>>',
                     reply_markup=settings_builder.as_markup()
                     # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())
                     )

async def call_help(call:types.CallbackQuery):
    help_builder = InlineKeyboardBuilder()
    help_builder.button(
        text='setngs',
        callback_data='my_set'
    )

    await call.message.edit_text(text='call_help>>>',
                                 reply_markup=help_builder.as_markup(resize_keyboard=True)
                                 # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())
                                 )