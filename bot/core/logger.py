import betterlogging

import betterlogging as logging
from logging.handlers import RotatingFileHandler

logging.basic_colorized_config(
    level=logging.INFO,
    # date="%H:%M:%S",
    handlers = [
        RotatingFileHandler(
            "ShemuraBot.log", maxBytes=(1024 * 1024 * 5), backupCount=10, encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(betterlogging.ERROR)

LOGS = logging.getLogger("ShemuraBot")

