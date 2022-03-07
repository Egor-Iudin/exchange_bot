from aiogram import Bot, Dispatcher, executor, types
from random import choices
from config import TOKEN, HELP_TEXT
from moex_client import api


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

test_db = {}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message) -> None:
    await message.reply("Привет!\nДля того, чтобы узнать, что умеет этот бот напиши /help!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message) -> None:
    await message.reply(HELP_TEXT)


@dp.message_handler(commands=['add'])
async def process_add_command(message: types.Message) -> None:
    data = await api()
    if len(message.text.split()) > 1:
        secids = message.text.split()[1:]
        data = [i for i in data if i[3] in secids]
        test_db[message.from_user.id] = {
            i: data[i] for i in range(len(secids))
        }
        curr_user_data = test_db[message.from_user.id]
        success = [curr_user_data[i][3]
                   for i in curr_user_data if curr_user_data[i][3] in secids]
        answer = ', '.join(success)
        await message.reply(f"Успешно добавлено:\n{answer}")
    else:
        await message.reply("Неправильный синтаксис, воспользуйтесть командой \help")


@dp.message_handler(commands=['show'])
async def process_show_command(message: types.Message) -> None:
    await message.reply("Вот Ваши добаленные котировки:\n")
    curr_user_data = test_db[message.from_user.id]
    answer = ''
    for i in range(len(curr_user_data)):
        answer += f"{curr_user_data[i][3]}: {curr_user_data[i][9]} rub.\n"
    await bot.send_message(message.from_user.id, answer)


@dp.message_handler(commands=['show_all'])
async def process_show_all_command(message: types.Message) -> None:
    await message.reply("Вот все доступные котировки:\n")
    data = await api()
    if len(message.text.split()) > 1 and len(data) > int(message.text.split()[1]):
        length = int(message.text.split()[1])
        data = choices(data, k=length)
    answer = ''
    for item in data:
        answer += f"{item[3]} -- {item[2]}\n"
    await bot.send_message(message.from_user.id, answer)


if __name__ == '__main__':
    executor.start_polling(dp)
