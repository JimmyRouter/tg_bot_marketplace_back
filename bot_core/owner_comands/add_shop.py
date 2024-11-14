from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from .forms import NewShopForm
from db_manager.manager import create_shop
from db_manager.models import Shop
from .markups import cancel_kboard
from .my_shop import shop_router


async def add_shop(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewShopForm.tittle)
    print('add_shop call', call)
    await call.message.answer(text='КАК ВЫ ХОТИТЕ НАЗВАТЬ НОВЫЙ МАГАЗИН?', reply_markup=cancel_kboard.as_markup())


@shop_router.message(NewShopForm.tittle)
async def add_shop_tag(msg: types.Message, state: FSMContext):
    await state.update_data(tittle=msg.text)
    await state.set_state(NewShopForm.token)
    await msg.answer(text='ВВЕДИТЕ ТОКЕН БОТА', reply_markup=cancel_kboard.as_markup())


@shop_router.message(NewShopForm.token)
async def add_shop_token(msg: types.Message, state: FSMContext):
    shop_info = await state.update_data(token=msg.text)
    shop_info.update({'owner_tg_id': str(msg.from_user.id)})
    # print('add_shop shop_info>>>>', shop_info)
    # print(" addshop Shop pydanted>>>>", shop_info)
    added = await create_shop(shop_info)
    # print('added shop_info>>>', added)
    await state.clear()
    await msg.answer(
        text='ДОБАВЛЕН',
        reply_markup=cancel_kboard.as_markup()
    )






