@echo off
cd venv\Scripts\
call activate.bat
cd ../..
cd tg_marketplace\tg_shop_bot_core\
uvicorn server_launcher:app --reload --port 8800
cmd /k
