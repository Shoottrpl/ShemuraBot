from math import ceil
from pyrogram.types import InlineKeyboardButton

from bot.core import Config, LOGS


def gen_inline_keyboard(collection: list, row: int = 2) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        key = []
        for j in collection[i : i + row]:
            button = btn(*j)
            key.append(button)
        keyboard.append(key)
    return keyboard

def btn(text, value, type="callback_data") -> InlineKeyboardButton:
    return InlineKeyboardButton(text, **{type: value})


async def gen_inline_help_buttons(page: int, plugins: list) -> tuple[list, int]:
    buttons = []
    column = 5
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    max_pages = ceil(len(pairs) / column)
    pairs = [pairs[i : i + column] for i in range(0, len(pairs), column)]

    for pair in pairs[page]:
        btn_pair = []
        for i, plugin in enumerate(pair):
            btn_pair.append(
                InlineKeyboardButton(f"{plugin}", f"help_menu:{page}:{plugin}")
            )
        buttons.append(btn_pair)
    buttons.append(
        [
            InlineKeyboardButton(
                f"help_page:{(max_pages - 1) if page == 0 else (page - 1)}",
            ),
            InlineKeyboardButton(
                f"help_data:c",
            ),
            InlineKeyboardButton(
                f"help_page:{0 if page == (max_pages - 1) else (page + 1)}",
            ),
        ]
    )

    return buttons, max_pages

async def gen_bot_help_buttons() -> list[list[InlineKeyboardButton]]:
    buttons = []
    plugins = sorted(Config.BOT_CMD_MENU)
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    for pair in pairs:
        btn_pair = []
        for plugin in pair:
            btn_pair.append(
                InlineKeyboardButton(f"{plugin}", f"bot_help_menu:{plugin}")
            )
        buttons.append(btn_pair)
    buttons.append(
        [
            InlineKeyboardButton("start", "help_data:start",),
            InlineKeyboardButton("close", "help_data:close",),
        ]
    )

    return buttons

def start_button() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton("HELP", "help_data:bothelp"),
            InlineKeyboardButton("SOURCE", "help_data:source")
            ],
    ]