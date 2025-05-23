import asyncio
import sys
import logging
from datetime import datetime
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from pydantic_settings import BaseSettings
from aiogram.types import FSInputFile, InputFile

from .keyboards.main_kb import main_menu_keyboard
from .keyboards.return_to_menu_kb import return_to_main_menu_keyboard
from .modules.api_connector import Connector as ApiConnector
from .modules.api_connector import Method, Get, Post, Put, Delete
from .modules.excel_manager import Manager as ExcelManager


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()  # for tbot routes
bot = None # aiogram bot obj
apiConnector = ApiConnector()  # for requests to api
settings = None  # Baseettings object from fast api part
API_URL = '' # API host
actions = {} # user actions manager
excelManager = ExcelManager()  # excel files manager (write and save)


# list of all commands which change notes (create, update etc.)
NOTE_COMMANDS = {
    'create': {
        'action': 'create',
        'answer': 'Send me your note using structure: \nCost (in UAH)\nDescription\nFor example:\n120\nFor some needs.'
    },
    'delete': {
        'action': 'delete',
        'answer': 'Send me id of note, which you want to delete.'
    },
    'edit': {
        'action': 'update',
        'answer': 'Send me your updated note using structure: \nId of note, which you want to edit\nCost (in UAH)\nDescription\n\nFor example:\n1\n120\nFor some needs.'
    },
}


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
    apiResponse = apiConnector.ask(f'{API_URL}/api/v1/getall/{user}')
    answer = ''

    if type(apiResponse) == dict:
        if apiResponse['data'] == []: answer += 'You dont have any notes!'
        else:
            answer += 'Your notes: \n'
            for note in apiResponse['data']:
                answer += f'{note['id']}) {round(note['summ'], 3)} ({round(note['summ2usd'], 3)}$, 1 USD = {note['currency']}) -> {note['description']}\n'
    elif type(apiResponse) == int:
        answer += f'Request to API gave a {apiResponse} status code!'
    else: answer += f'Request to API gave a \n"{apiResponse}"'

    await message.answer(answer, reply_markup=main_menu_keyboard)


@dp.message(F.text.lower() == "return")
async def cmd_return_to_main_menu(message: types.Message):
    global actions
    actions[message.from_user.id] = ''

    await message.answer(
        'You`re in main menu.', reply_markup=main_menu_keyboard
    )


# an ordinary variable name in da hood
@dp.message(F.text.lower() == "download .xlsx")
async def cmd_download_my_notes_as_xlsx_file_without_ads_and_sms_please(message: types.Message):
    user = message.from_user.id

    # getting my notes
    apiResponse = apiConnector.ask(f'{API_URL}/api/v1/getall/{user}')

    if type(apiResponse) != dict:
        await message.answer(f'Cannot get your notes from API!\nResponse: {apiResponse}')
        return 0

    wb, sheet = excelManager.createWorkbook()
    noteId = 2
    await message.answer('Creating excel file...')

    for note in apiResponse['data']:
        excelManager.write(sheet, 'A', noteId, note['id']) # write id
        excelManager.write(sheet, 'B', noteId, note['created_at']) # write date
        excelManager.write(sheet, 'C', noteId, note['summ']) # write price
        excelManager.write(sheet, 'D', noteId, note['summ2usd']) # write price in ud
        excelManager.write(sheet, 'E', noteId, note['currency']) # write currency (price for 1 usd)
        excelManager.write(sheet, 'F', noteId, note['description']) # write description

        noteId += 1

    # saving new file
    filename = f'{datetime.now().strftime("%H-%M-%S %Y-%m-%d")}__{user}.xlsx'
    excelManager.save(wb, filename)
    fileForUplodaing: InputFile = FSInputFile(path=filename)

    await bot.send_document(user, fileForUplodaing)
    os.remove(filename)


# global text checker (will check all messages, also for commands from NOTE_COMMANDS)
# IT MUST BE ONLY ONE GLOBAL CHECKER FOR MESSAGES HERE!
@dp.message()
async def global_text_handler(message: types.Message):
    global actions

    user = message.from_user.id
    text = message.text
    lowerMessageText = message.text.lower()
    response = None # future response from API
    answer = '' # text, which will send to user

    # because i cannot just put this condition in dp.message decorator
    # only for NOTE_COMMANDS
    if lowerMessageText in list(NOTE_COMMANDS.keys()):
        user = message.from_user.id

        actions[user] = NOTE_COMMANDS[lowerMessageText]['action']
        await message.answer(NOTE_COMMANDS[lowerMessageText]['answer'], reply_markup=return_to_main_menu_keyboard)
        return None

    # checking for correct signature
    try:
        if actions.get(user) == 'create':
            price, description = text.split('\n')
            price = int(price)

            response = apiConnector.ask(
                f'{API_URL}/api/v1/create',
                Post, header={"Content-Type": "application/json"},
                body={
                    "lineData": {
                        "summ": price,
                        "description": description,
                        "created_by": str(user)
                    }
                }
            )
        elif actions.get(user) == 'update':
            noteId, price, description = text.split('\n')
            noteId, price = int(noteId), int(price)

            response = apiConnector.ask(
                f'{API_URL}/api/v1/update/{noteId}',
                Put, header={"Content-Type": "application/json"},
                body={
                    "updateInfo": {
                        "summ": price,
                        "description": description,
                        "created_by": str(user)
                    }
                }
            )
        elif actions.get(user) == 'delete':
            noteId = int(message.text)

            response = apiConnector.ask(
                f'{API_URL}/api/v1/delete/{noteId}', Delete
            )

        else: # unknown message
            await message.answer('You`re in main menu.', reply_markup=main_menu_keyboard)
            return None

    except: await message.answer('Incorrect structure! Cannot parse your message.', reply_markup=return_to_main_menu_keyboard)
    else:
        actions[user] = ''

        # answer (include response info)
        if type(response) == dict: answer = 'Done'
        elif type(response) == int: # returned error satus code
            answer = f'Error! Please, try again later.\nStatus code from API: {response}'
        else:
            answer = f'Incorrect response from API!\nResponse: {response}'

        # sending answer to user
        await message.answer(answer, reply_markup=main_menu_keyboard)




def getArgument(l: list, arg_name: str) -> None|str:
     arg = l[l.index(arg_name) + 1]
     if arg: return arg


async def startTelegramBot(_settings: BaseSettings):
    global settings
    global API_URL
    global bot

    settings = _settings
    API_URL = f'http://{settings.api_host if settings.api_host != '0.0.0.0' else '127.0.0.1'}:{settings.api_port}'

    bot = Bot(token=settings.telegram_bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    token = getArgument(sys.argv, '-t')
    if not token:
        print('Cannot detect token. Please set token using "-t [TOKEN]".')
        sys.exit(1)

    asyncio.run(startTelegramBot(token))
