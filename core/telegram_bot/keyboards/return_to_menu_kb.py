from aiogram import types



return_to_main_menu_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder='Make your choice',
    keyboard=[
        [types.KeyboardButton(text="Return")]
    ]
)