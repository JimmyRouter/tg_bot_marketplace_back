from datetime import datetime
from enum import Enum
from random import randint
from typing import List, Any, Union
from pydantic import BaseModel, Field

from db_manager.connector import generate_objectId


class DefaultModel(BaseModel):
    id: int = Field(default_factory=generate_objectId().__await__, alias='_id')
    created: datetime = datetime.now()

class Rating(BaseModel):
    value: float = 5
    rate: int = 5
    votes: int = 0

    # def increase_rating(rate):
    #     votes += 1
    #     value = (value + rate) / votes


class Size(str, Enum):
    pc1 = '1 pc'
    pc3 = '3 pc'
    pc10 = '10 pc'
    kg1 = '1 kg'
    kg10 = '10 kg'


class Product(DefaultModel):
    tittle: str = 'Name of the Product'
    description: str = 'description of the Product'
    img: str = 'EMPTY.jpg'
    rating: Rating = Rating()
    is_active: bool = False


class Category(DefaultModel):
    tittle: str = 'Name of Category'
    description: str = 'Description of the Category'
    img: str = 'EMPTY.jpg'
    products: List[Product] = []


class Shop(DefaultModel):
    tg_id: int = randint(1000, 9999999)     # DEBUG mode
    owner_tg_id: int
    username: str = '@Telegram_Username_here'
    tittle: str = 'Shop name'
    description: str = 'Shop description'
    is_running: bool = False
    token: str = 'telegram token'       # SECURITY WARN  encript or else...
    catalog: List[Category] = []
    img: str = 'EMPTY.jpg'


class TGUser(DefaultModel):
    tg_id: int = 0
    username: str
    first_name: str = 'noname'
    last_name: str = 'nolast'
    is_bot: bool = False
    is_premium: Any
    language_code: str
    role: List[str] = []
    disabled: bool = True


class Curency(dict, Enum):
    USD = {
        'title':'USD',
        'rate':1,

    }
    RUB = {
        'title': 'USD',
        'rate': 100,

    }
    LARI = {
        'title': 'USD',
        'rate': 2.7,

    }


class Package(DefaultModel):
    shop: int
    category: int
    product: int
    size: Size = Size.pc1
    price: float = 100.00
    curency: Curency = Curency.USD
    location: str = ''
    img1: str = ''
    img2: str = ''
    img3: str = ''
    reserved: bool = False


class Order(DefaultModel):
    cart: List[Package] = []
    client: TGUser
    status: Union['pending | payed | finished | ticket'] = 'pending'


class Deal(DefaultModel):
    order: Order
    success: bool = True


class Role(dict, Enum):
    SUPERUSER = {
        'type': 'SUPERUSER',
        'permissions':[
            ('TGUser','crud'),
            ('Shop', 'crud'),
            ('Staff', 'crud'),
            ('Category', 'crud'),
            ('Product', 'crud'),
            ('Package','crud'),
            ('Order', 'crud'),
        ],
        'restrict': None,

    }
    ADMIN = {
        'type': 'ADMIN',
        'permissions': [
            ('Shop', 'ru'),
            ('Staff', 'crud'),
            ('Category', 'crud'),
            ('Product', 'crud'),
            ('Package', 'crud'),
            ('Order', 'crud'),

        ],
        'restrict': 'Shop'
    }
    MANAGER = {
        'type': 'MANAGER',
        'permissions': [
            ('Shop', 'ru'),
            ('Staff', 'cr'),
            ('Category', 'cru'),
            ('Product', 'cru'),
            ('Package', 'r'),
            ('Order', 'cru'),

        ],
        'restrict': 'Shop'
    }
    NEW_STAFF = {
        'type': 'NEW_STAFF',
        'permissions': [
            ('Shop', 'r'),
        ],
        'restrict': 'Shop'
    }


class Staff(DefaultModel):
    username: str = ''
    email: str = ''
    role: Role = Role.NEW_STAFF
    disabled: bool = True


#=================AUTH======================#

class StaffInDb(Staff):
    hashed_pwd: str = 'nohash'   #SECURITY WARN


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
