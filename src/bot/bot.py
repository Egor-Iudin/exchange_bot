from cgitb import handler
from aiogram import Bot, Dispatcher, executor, types
from random import choices
from config import TOKEN, HELP_TEXT, COLUMNS_NAME
from aiogram.types import ParseMode

from src.moex_client.api import api
from table_builder import make_table  # TODO: refactor!!!
from db.base import get_mongo_client
from db.handlers import (
    create_user_handler,
    fetch_one_user_handler,
    add_user_stocks_handler,
    delete_user_stocks_handler
)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
mongo_client = get_mongo_client()
mongo_db = mongo_client.users


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message) -> None:
    await message.reply("Привет!\nДля того, чтобы узнать, что умеет этот бот напиши /help!")
    if not await fetch_one_user_handler(mongo_db, message.from_user.id):
        await create_user_handler(mongo_db, message.from_user.id)


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message) -> None:
    await message.reply(HELP_TEXT)


@dp.message_handler(commands=["add"])
async def process_add_command(message: types.Message) -> None:
    data = await api()
    user = await fetch_one_user_handler(mongo_db, message.from_user.id)
    stocks = user["stocks"]
    user_input = message.text.split()
    if len(user_input) > 1:
        secids = user_input[1:]
        to_add = [i[COLUMNS_NAME["Symbol"]]
                  for i in data if i[COLUMNS_NAME["Symbol"]] in secids and i[COLUMNS_NAME["Symbol"]] not in stocks]
        if to_add:
            await add_user_stocks_handler(mongo_db, message.from_user.id, to_add)

            answer = ", ".join(to_add)
            await message.reply(f"Успешно добавлено:\n{answer}\nВсего новых: {len(to_add)}")
        else:
            await message.reply(f"Таких котировок нет или они уже были добавдены!")
    else:
        await message.reply("Неправильный синтаксис, воспользуйтесть командой \help!")


@dp.message_handler(commands=["remove"])
async def process_remove_command(message: types.Message) -> None:
    user = await fetch_one_user_handler(mongo_db, message.from_user.id)
    stocks = user["stocks"]
    user_input = message.text.split()
    if len(user_input) > 1:
        secids = user_input[1:]
        to_delete = [i for i in secids if i in stocks]
        if to_delete:
            await delete_user_stocks_handler(mongo_db, message.from_user.id, to_delete)
            answer = ", ".join(to_delete)
            await message.reply(f"Успешно удалено:\n{answer}")
        else:
            await message.reply(f"Таких котировок у Вас нет или они уже были удалены!")
    else:
        await message.reply("Неправильный синтаксис, воспользуйтесть командой /help!")


@dp.message_handler(commands=["show"])
async def process_show_command(message: types.Message) -> None:
    user = await fetch_one_user_handler(mongo_db, message.from_user.id)
    stocks = user["stocks"]
    data = await api()
    data = [i for i in data if i[COLUMNS_NAME["Symbol"]] in stocks]
    if not stocks:
        await message.reply("Вы еще ничего не добавили!\n")
    else:
        await message.reply("Вот Ваши добаленные котировки:\n")
        table = make_table(message, data, ["Symbol", "ClosePrice"])
        await message.answer(f"<pre>{table}</pre>", parse_mode=ParseMode.HTML)


@dp.message_handler(commands=["show_all"])
async def process_show_all_command(message: types.Message) -> None:
    await message.reply("Вот все доступные котировки:\n")
    data = await api()
    if len(message.text.split()) > 1:
        user_input = message.text.split()[1]
        if user_input.isdigit():
            length = int(user_input)
            if length < len(data):
                data = choices(data, k=length)
        else:
            await message.answer(f"Если хотите ограничить вывод, нужно ввести целое число (\help)!")
    table = make_table(message, data, ["Symbol", "ShortName"])
    await message.answer(f"<pre>{table}</pre>", parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    executor.start_polling(dp)
