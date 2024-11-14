import logging
import asyncio
from aiogram import Dispatcher, Bot
import constants
from bot_core.bot_routers.client_router import client_router, client_msg_cmds, client_call_cmds
from bot_core.bot_routers.owner_router import owner_router
from bot_core.owner_comands import owner_call_cmds, owner_msg_cmds

from aiogram import Router, F


def register_commands(router: Router,
                      commands: [],
                      mode: str) -> None:

    if mode == "msg":
        for cmd in commands:
            router.message.register(cmd[0], F.text == cmd[1])
        return
    if mode == "call":
        for cmd in commands:
            router.callback_query.register(cmd[0], F.data == cmd[1])
        return


dp = Dispatcher()
dp.include_router(owner_router)
bot = Bot(token=constants.TG_API_KEY)
# bot.download()

async def bot_poll():
    logging.basicConfig(level=logging.DEBUG)
    commamds_for_bot = []

    print('bot launcher get me>>>>>>', await bot.get_me())
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(commamds_for_bot)
    register_commands(dp, client_msg_cmds, mode='msg')
    register_commands(client_router, client_call_cmds, mode='call')

    register_commands(dp, owner_msg_cmds, mode='msg')
    register_commands(owner_router, owner_call_cmds, mode='call')

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(bot_poll())
    except(KeyboardInterrupt, SystemExit):
        print('STOPPED')

