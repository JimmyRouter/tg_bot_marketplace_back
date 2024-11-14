from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer


TG_API_KEY = 'your api key'  #TODO .env
TG_WEBAPP_URI ='your web app url'  #TODO .env
TELEGRAM_API_ENDPOINT = 'https://api.telegram.org/'

BOT_COMMANDS = (
    ("start", "начало работы", "Запускает бота, введите /start для перезагрузки или запуска этого бота"),
    ("help", "справка о командах", "Выводит описание комманд, введите /help и название команды для вывода справки"),

)
MONGO_SERVER = {'host': 'localhost', 'port': 27150}
DEFAULT_SHOP_ID = 36    # for debug, remove

SECRET_KEY = "CVEwrsDT9kJDNbrwb7hweJk9tn0RBKverF56uiB6Nj59gF$6dn5fr8W7r"  #TODO .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth")

CREDENTIALS_EXEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

ROLE_EXEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Вы попытались попасть в запретную зону, оставайтесь на месте и дожидайтесь спецотряд по зачистке",
        headers={"WWW-Authenticate": "Bearer"},
    )