from aiogram import Router
from bot_core.client_commands.start import start
from bot_core.client_commands.start_app import start_app
from bot_core.client_commands.my_orders import my_orders
from bot_core.client_commands.help import help_command

client_router = Router(name="client_router")

client_msg_cmds = [
    (start, 'start'),
    (help_command, 'help')
]

client_call_cmds = [
    (start_app, 'start_app'),
    (my_orders, 'my_orders'),
]

