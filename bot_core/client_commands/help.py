import pprint
from aiogram import types
from aiogram.filters import CommandObject
import constants


async def help_command(msg: types.Message):
    print('help_command>>>>')
    for m in msg:
        print(m)

    print('help_command>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<,')
    try:
        cmd = msg.text.split(' ')[1]
        print('cmd in help>>>>>>>>>>>>>',cmd)
        for c in constants.BOT_COMMANDS:
            if c[0] == cmd:
                return await msg.answer(f'{c[0]}--{c[1]}\n\n{c[2]}')
            else:
                return await msg.answer('такой команды нет')
    except:
        return await msg.answer('введите /help <комманда> для справки')