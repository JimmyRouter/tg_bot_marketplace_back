from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from db_manager.manager import add_cat
from .markups import cancel_kboard
from .forms import NewCategoryForm
from ..custom_callbacks import TGCategory


add_cat_router = Router(name='add_cat_router')


@add_cat_router.callback_query(TGCategory.filter(F.view == 'add_cat'))
async def add_category(call: types.CallbackQuery, callback_data: TGCategory, state: FSMContext):
    await state.update_data(shop_id=callback_data.shop_id)
    await state.set_state(NewCategoryForm.tittle)
    await call.message.answer(text='Send name of the Category', reply_markup=cancel_kboard.as_markup())


@add_cat_router.message(NewCategoryForm.tittle)
async def add_category_img(msg: types.Message, state: FSMContext):
    if msg.text:
        await state.update_data(tittle=msg.text)
        await state.set_state(NewCategoryForm.description)
        await msg.answer(text='Send short Category description', reply_markup=cancel_kboard.as_markup())
    else:
        await msg.answer(text='Send TEXT MESSAGE with name of the Category', reply_markup=cancel_kboard.as_markup())


@add_cat_router.message(NewCategoryForm.description)
async def add_category_img(msg: types.Message, state: FSMContext):
    if msg.text:
        await state.update_data(description=msg.text)
        await state.set_state(NewCategoryForm.img)
        await msg.answer(text='Send Photo of the Category', reply_markup=cancel_kboard.as_markup())
    else:
        await msg.answer(text='Send TEXT MESSAGE with short Category description', reply_markup=cancel_kboard.as_markup())

@add_cat_router.message(NewCategoryForm.img)
async def added_category_img(msg: types.Message, state: FSMContext):
    if msg.photo:
        cat_info = await state.update_data(img=msg.photo[-1].file_id)
        print('added_cat_img cat>>>>>', cat_info)
        added = await add_cat(cat_info, cat_info['shop_id'])
        await state.clear()
        await msg.answer(text='Category added successfully', reply_markup=cancel_kboard.as_markup())  # TODO Check if success
    else:
        await msg.answer(text='ATTACH Photo of the Category and send to this chat', reply_markup=cancel_kboard.as_markup())