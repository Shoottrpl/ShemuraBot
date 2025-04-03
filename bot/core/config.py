from os import getenv

from dotenv import load_dotenv
from pyrogram import filters
from pathlib import Path
from os.path import dirname

load_dotenv()

class Config:
    API_ID = int(getenv("API_ID", 0))
    API_HASH = getenv("API_HASH", None)
    BOT_TOKEN = getenv("BOT_TOKEN", None)
    LOGGER_ID=getenv("LOGGER_ID", 0)
    ROOT = Path(dirname(__file__)).resolve().parents[1]
    WORKDIR = Path(dirname(__file__)).parent
    SESSIONS_FILE = WORKDIR / "sessions" / "sessions.json"
    DWNL_DIR = "./downloads/"

    #git
    GIT_REP = getenv("GIT_REP", None)

    #user config
    AUTH_USERS=filters.user()
    CRYPT_KEY=getenv("CRYPT_KEY")

    #global
    HELP_DICT = {}
    CMD_INFO = {}
    CMD_MENU = {}
    BOT_CMD_MENU = {}
    BOT_CMD_INFO = {}
    BOT_HELP = {}





class Symbols:
    anchor = "✰"
    arrow_left = "↞"
    arrow_right = "↠"
    back = "☜ ʙᴀᴄᴋ"
    bullet = "•"
    check_mark = "✓"
    close = "❌ 𝗖𝗟𝗢𝗦𝗘 ❌"
    cross_mark = "✗"
    diamond_1 = "◇"
    diamond_2 = "◈"
    next = "⤚ ɴᴇxᴛ"
    previous = "ᴘʀᴇᴠ ⤙"
    radio_select = "◉"
    radio_unselect = "〇"
    triangle_left = "◂"
    triangle_right = "▸"