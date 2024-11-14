from aiogram.filters.callback_data import CallbackData


class TestCall(CallbackData, prefix='testcall'):
    shop_id: int
    view: str = 'test'


class TGProduct(CallbackData, prefix='tgproduct'):
    view: str = 'myproduct'
    shop_id: int
    cat_id: int
    id: int = 0


class TGCategory(CallbackData, prefix='tgcat'):
    view: str = 'my_cat'
    shop_id: int
    id: int = 1
    tittle: str = 'cat'


class TGShop(CallbackData, prefix='tgshop'):
    view: str
    id: int
    tg_id: int
    tittle: str


class TGPackage(CallbackData, prefix='tgpack'):
    view: str = 'mypackage'
    shop_id: int
    cat_id: int
    prod_id: int
    size: str
    id: int = 0

