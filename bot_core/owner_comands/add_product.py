from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from db_manager.manager import add_prod
from .markups import cancel_kboard
from .forms import NewProductForm
from ..custom_callbacks import TGProduct

add_prod_router = Router(name='add_prod_router')

@add_prod_router.callback_query(TGProduct.filter(F.view == 'add_prod'))
async def add_product(call: types.CallbackQuery, callback_data: TGProduct, state: FSMContext):
    await state.update_data(shop_id=callback_data.shop_id)
    await state.update_data(cat_id=callback_data.cat_id)
    await state.set_state(NewProductForm.tittle)
    await call.message.answer(text='Enter Product name', reply_markup=cancel_kboard.as_markup())


@add_prod_router.message(NewProductForm.tittle)
async def add_product_img(msg: types.Message, state: FSMContext):
    if msg.text:
        await state.update_data(tittle=msg.text)
        await state.set_state(NewProductForm.img)
        await msg.answer(text='Send Product photo', reply_markup=cancel_kboard.as_markup())
    else:
        await msg.answer(text='Send text message to this chat with the NAME of the Product',
                         reply_markup=cancel_kboard.as_markup())


@add_prod_router.message(NewProductForm.img)
async def added_product_img(msg: types.Message, state: FSMContext):
    if msg.photo:
        photo_id = msg.photo[-1].file_id
        product = await state.update_data(img=photo_id)
        added = await add_prod(prod=product, shop_id=product['shop_id'], cat_id=product['cat_id'])
        await state.clear()
        await msg.answer(text='ПРОДУКТ ДОБАВЛЕН', reply_markup=cancel_kboard.as_markup())
    else:
        await msg.answer(text='ПРИКРЕПИТЕ ФОТОГРАФИЮ ТОВАРА И ОТПРАВЬТЕ В ЧАТ',
                         reply_markup=cancel_kboard.as_markup())
