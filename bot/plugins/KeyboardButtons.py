from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup


def gen_keyboard(collection: list, row: int = 2) -> list[list[KeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        key = []
        for j in collection[i : i + row]:
            key.append(KeyboardButton(j))
        keyboard.append(key)
    return keyboard


def session_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("New"),
                KeyboardButton("Delete"),
            ],
            [
                KeyboardButton("List"),
                KeyboardButton("Home"),
            ]
        ],
        resize_keyboard=True,
    )


def start_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("SESSION"),
                KeyboardButton("FORCE SUB"),
            ],
            [
                KeyboardButton("USERS"),
                KeyboardButton("OTHER"),
            ],
        ],
        resize_keyboard=True,
    )

