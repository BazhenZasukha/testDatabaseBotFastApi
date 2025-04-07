import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F

from .keyboards.main_kb import main_menu_keyboard


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Hello! Im your notes manager. I will collect all your notes about your costs :3",
        reply_markup=main_menu_keyboard
    )

@dp.message(F.text.lower() == "my notes")
async def cmd_my_notes(message: types.Message):
    user = message.from_user.id



def getArgument(l: list, arg_name: str) -> None|str:
     arg = l[l.index(arg_name) + 1]
     if arg: return arg

async def startTelegramBot(token: str):
    bot = Bot(token=token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    token = getArgument(sys.argv, '-t')
    if not token:
        print('Cannot detect token. Please set token using "-t [TOKEN]".')
        sys.exit(1)

    asyncio.run(startTelegramBot(token))
