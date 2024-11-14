from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .markups import cancel_kboard
from fastapi_server.utility_functions import dowload_file
from bot_core.owner_comands.forms import TestForm
from ..custom_callbacks import TestCall


test_router = Router(name='test_router')


@test_router.callback_query(TestCall.filter(F.view == 'test'))
async def test(call: types.CallbackQuery, callback_data: TestCall, state: FSMContext):
    # await state.update_data(shop_id=callback_data.shop_id)
    # await state.set_state(TestForm.photo)
    # print('test>>call:>>>', call)
    await call.message.answer(text='сказал же не лазать))')


# @test_router.message(TestForm.photo)
async def test_photo(msg: types.Message, state: FSMContext):
    st = await state.update_data(photo=msg.photo)
    shop_id = st['shop_id']
    # await dowload_file(msg.photo[-1].file_id, shop_id)

    await state.clear()
    k_board = InlineKeyboardBuilder()
    k_board.attach(cancel_kboard)
    k_board.button(
        text='again',
        callback_data=TestCall(shop_id=shop_id)
    )
    await msg.answer(text='заново', reply_markup=k_board.as_markup())

