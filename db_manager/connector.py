import motor.motor_asyncio
from constants import MONGO_SERVER


client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(MONGO_SERVER['host'], MONGO_SERVER['port'])
market_db: motor.motor_asyncio.AsyncIOMotorDatabase = client['marketplace']
staff_cll: motor.motor_asyncio.AsyncIOMotorCollection = market_db['staff']
users_cll: motor.motor_asyncio.AsyncIOMotorCollection = market_db['clients']
shops_cll: motor.motor_asyncio.AsyncIOMotorCollection = market_db['shops']
orders_cll: motor.motor_asyncio.AsyncIOMotorCollection = market_db['orders']


async def generate_objectId():
    last_id = await market_db.obj_ids.find_one({'id_type': 'last_id'},
                                       {'_id': 0,
                                        'value': 1
                                        })
    lid = last_id['value']
    new_id = lid + 1 # noqa
    updated = await market_db['obj_ids'].update_one({'id_type': 'last_id'},
                                                          {'$set': {'value':new_id}}
                                                          )
    if updated.acknowledged:
        return new_id
    else:
        return None
