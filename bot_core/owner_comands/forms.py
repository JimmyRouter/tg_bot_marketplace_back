from aiogram.fsm.state import State, StatesGroup

class NewShopForm(StatesGroup):
    tittle = State()
    token = State()


class NewCategoryForm(StatesGroup):
    shop_id = State()
    tittle = State()
    description = State()
    img = State()


class NewProductForm(StatesGroup):
    shop_id = State()
    cat_id = State()
    tittle = State()
    img = State()


class TestForm(StatesGroup):
    shop_id = State()
    photo = State()




