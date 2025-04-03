from .clients import ShemuraBot
from .config import Config
from .logger import LOGS

async def _AuthUsers() -> None:
    temp_list = []
    temp_list.extend([(await client.get_me()).id for client in ShemuraBot.users])

    users = list(set(temp_list))
    for user in users:
        Config.AUTH_USERS.add(user)

    temp_list = None
    LOGS.info("Added Authorized Users")


async def UserSetup() -> None:
    LOGS.info("Setting Up Users")
    await _AuthUsers()

