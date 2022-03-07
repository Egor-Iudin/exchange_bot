import os


DEBUG = int(os.getenv("DEBUG"))

TOKEN = os.getenv("TOKEN")

MONGO_USER = os.getenv("MONGO_USER")
MONGO_USER_PASSWORD = os.getenv("MONGO_USER_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

HELP_TEXT = '''Команды:\n
/add [options: str] - добавить котировки\n
/remove [options: str] - удалить котировки\n
/show - показывает все ваши котровки\n
/show_all [number: int] - показывает number котировко, если число котировок не указано, то выводятся все доступные'''

COLUMNS_NAME = {
    "Symbol": 3,
    "ClosePrice": 9,
    "ShortName": 2,
}
