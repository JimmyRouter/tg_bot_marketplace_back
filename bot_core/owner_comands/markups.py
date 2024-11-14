from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.utils.web_app import WebAppInitData

from bot_core.custom_callbacks import TestCall
from bot_core.owner_comands.forms import TestForm
import constants
index_markup = InlineKeyboardBuilder()
index_markup.button(text='      ✅ МОИ МАГАЗИНЫ         ',
                    callback_data='my_shops',)
index_markup.button(text='✅       ОБРАЗЕЦ            ',
                    web_app=WebAppInfo(url='https://testing1-bice.vercel.app/'))
index_markup.button(text='✅       ТЕСТ        ',
                    callback_data=TestCall(shop_id='6808139269'))

index_markup.adjust(1, 1, 1)

cancel_kboard = InlineKeyboardBuilder()
# canc = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ОТМЕНА', callback_data='w_start_app')]])
cancel_kboard.row(InlineKeyboardButton(text='ОТМЕНА', callback_data='w_start_app'))


