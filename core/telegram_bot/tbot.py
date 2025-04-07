import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from pydantic_settings import BaseSettings

from .keyboards.main_kb import main_menu_keyboard
from .modules.api_connector import Connector as ApiConnector
from .modules.api_connector import Method, Get, Post, Put, Delete


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
apiConnector = ApiConnector()
settings = None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Hello! Im your notes manager. I will collect all your notes about your costs :3",
        reply_markup=main_menu_keyboard
    )


# routes for main menu keyboard buttons

# get all notes from current user
@dp.message(F.text.lower() == "my notes")
async def cmd_my_notes(message: types.Message):
    user = message.from_user.id
    apiResponse = apiConnector.ask(f'http://{settings.api_host if settings.api_host != '0.0.0.0' else '127.0.0.1'}:{settings.api_port}/api/v1/getall/{user}')
    answer = ''

    if type(apiResponse) == dict:
        if apiResponse['data'] == []: answer += 'You dont have any notes!'
        else:
            answer += 'Your notes: '
            for note in apiResponse['data']:
                answer += f'{note['id']}) {note['summ']} ({note['summ2usd']}USD, 1 USD = {note['currency']}) -> {note['description']}\n'
    elif type(apiResponse) == int:
        answer += f'Request to API gave a {apiResponse} status code!'
    else: answer += f'Request to API gave a \n"{apiResponse}"'

    await message.answer(answer, reply_markup=main_menu_keyboard)




def getArgument(l: list, arg_name: str) -> None|str:
     arg = l[l.index(arg_name) + 1]
     if arg: return arg


async def startTelegramBot(_settings: BaseSettings):
    global settings
    settings = _settings

    bot = Bot(token=settings.telegram_bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    token = getArgument(sys.argv, '-t')
    if not token:
        print('Cannot detect token. Please set token using "-t [TOKEN]".')
        sys.exit(1)

    asyncio.run(startTelegramBot(token))
