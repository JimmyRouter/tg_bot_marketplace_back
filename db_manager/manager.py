from aiogram import types
from datetime import datetime

from pydantic import BaseModel

from fastapi_server.utility_functions import dowload_file
from .connector import users_cll, orders_cll, shops_cll, market_db, generate_objectId
from .models import Product, Category, TGUser, Shop, Package
from constants import DEFAULT_SHOP_ID


async def dump_model(model_item: BaseModel):   # default mongo _id is too long for aiogram
    new_item = model_item.model_dump()
    new_item.update({'_id': await generate_objectId()})
    return new_item


async def extract_data(query: types.Message | types.CallbackQuery):
    match type(query):
        case types.CallbackQuery:
            user_id = query.from_user.id
            shop_id = query.message.from_user.id

        case types.Message:
            user_id = query.from_user.id
            shop_id = None
        case _:
            return None
    return user_id, shop_id


async def checkin(call: types.CallbackQuery, role: str = 'client'):
    userid, shopid = await extract_data(call)
    user = await users_cll.find_one({'tg_id': userid})
    if user:
        if role in user['role']:
            return user
        else:
            return await users_cll.update_one({'_id': user['_id']}, {'$push': {'role': role}})  # adds role

    new_user_info = {
        'tg_id': userid,
        'username': call.from_user.username,
        'first_name': call.from_user.first_name,
        'last_name': 'nolast',                               #call.from_user.last_name,
        'is_bot': call.from_user.is_bot,
        'is_premium': call.from_user.is_premium,
        'language_code': call.from_user.language_code,
        'created': datetime.now(),
        'role': [role]
    }
    new_user = TGUser(**new_user_info)
    print('checkin>> new user>>>>>', new_user)
    ins_user = await dump_model(new_user)
    return await users_cll.insert_one(ins_user)


async def get_client_orders(tg_id, shop_id):
    return await orders_cll.find({
        {'client_tg_id': tg_id,
         'shop_tg_id': shop_id,
         }
    }).to_list()


async def getshop(shop_id):
    return await shops_cll.find_one(
        {'_id': int(shop_id)},
        {'_id': 1, 'token': 0},
    )


async def get_owner_shops(owner_tg_id):
    return await shops_cll.find({'owner_tg_id': owner_tg_id},
                                {
                                 'token': 0,
                                 }
                                ).to_list(100)


async def get_shop_categories(shop_id):
    shop = await shops_cll.find_one({'_id': shop_id},
                                    {'catalog': 1}
                                    )
    if shop:
        return shop['catalog']
    else:
        return []


async def get_products(shop_id, cat_id):
    shop = await shops_cll.find_one({'_id': shop_id,
                                     },
                                    {'catalog': 1}
                                    )

    for cat in shop['catalog']:   # todo improve to mongo request
        if cat['_id'] == cat_id:
            prods = cat['products']
            return prods


async def get_categories(shop_id=DEFAULT_SHOP_ID):
    shop = await shops_cll.find_one({'_id': shop_id,
                                     },
                                    {'catalog': 1}
                                    )
    if shop:
        cats = []  # TODO ??? old version api?
        for cat in shop['catalog']:
            cats.append(cat['tittle'])

        return shop['catalog']
    return False


async def get_prod(shop_id, cat_id, prod_id):
    products = await get_products(shop_id, cat_id)   # TODO optimize request to db
    for prod in products:
        if prod['_id'] == prod_id:
            return prod


async def add_cat(cat: dict, shop_id: int):

    img_name = await dowload_file(cat['img'], shop_id=shop_id)
    cat['img'] = img_name
    new_cat = Category(**cat)
    ins_cat = await dump_model(new_cat)
    updated = await shops_cll.update_one(
        {'_id': shop_id},
        {'$push': {'catalog': ins_cat}}
    )
    return        # TODO success check


async def add_prod(prod: dict, shop_id: int, cat_id: int):
    img_name = await dowload_file(prod['img'], shop_id=shop_id)
    prod['img'] = img_name
    new_prod = Product(**prod)
    ins_prod = await dump_model(new_prod)
    # query = {'_id': shop_id}
    # update = {'$push': {f'catalog.{cat_id}.products': ins_prod}}
    return await shops_cll.update_one(
        {'_id': shop_id,},                                  # query
        {'$push': {'catalog.$[elem].products': ins_prod}},  # update
        array_filters=[{'elem._id': cat_id}]                #
    )


async def add_pack(pack: dict):
    pack = Package(**pack)
    ins_pack = await dump_model(pack)
    return await shops_cll.update_one(
        {'_id': pack.shop},
        {'$push': {'packs': ins_pack}},
    )


async def create_shop(shop_info):
    new_shop = Shop(**shop_info)
    ins_shop = await dump_model(new_shop)
    return await shops_cll.insert_one(ins_shop)


async def delete_instance(model_name: str, **kwargs):
    model_id = kwargs['shop_id']
    match model_name.lower():
        case 'shop':                      # Add your delete cases
            shops_cll.delete_one(
                {'_id': model_id}
            )
            return model_id
        case _:
            return 0
