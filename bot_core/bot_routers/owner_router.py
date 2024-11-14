from aiogram import Router, types, F

from bot_core.owner_comands.add_category import add_cat_router
from bot_core.owner_comands.add_product import add_prod_router
from bot_core.owner_comands.my_categories import categories_router
from bot_core.owner_comands.my_category import my_cat_router
from bot_core.owner_comands.my_product import my_prod_router
from bot_core.owner_comands.my_shop import shop_router
from bot_core.owner_comands.test import test_router

owner_router = Router(name="owner_router")

my_cat_router.include_router(add_prod_router)
my_cat_router.include_router(my_prod_router)
categories_router.include_router(add_cat_router)
categories_router.include_router(my_cat_router)
shop_router.include_router(categories_router)
# shop_router.include_router(add_cat_router)

owner_router.include_router(shop_router)

owner_router.include_router(test_router)



