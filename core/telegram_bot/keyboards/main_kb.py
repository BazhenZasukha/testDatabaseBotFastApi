from aiogram import types



main_menu_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder='Make your choice',
    keyboard=[
        [types.KeyboardButton(text="My notes")],
        [
            types.KeyboardButton(text="Delete"),
            types.KeyboardButton(text="Edit"),
            types.KeyboardButton(text="Create")
        ],
        [types.KeyboardButton(text="Download .xlsx")]
    ]
)