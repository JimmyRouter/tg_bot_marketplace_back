from bot_core.owner_comands.add_category import add_category
from bot_core.owner_comands.test import test
from bot_core.owner_comands.w_start import w_start
from bot_core.owner_comands.my_shops import my_shops
from bot_core.owner_comands.w_start_app import w_start_app
from bot_core.owner_comands.add_shop import add_shop

owner_msg_cmds = [
    (w_start, '/start'),
]

owner_call_cmds = [
    (w_start_app, 'w_start_app'),
    (my_shops, 'my_shops'),
    (add_shop, 'add_shop'),
    # (add_category, 'add_category'),
    # (add_product, 'add_product'),
    # (test, 'test')
]

