import asyncio
import sys
import logging
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


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
