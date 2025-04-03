import os
import json
from pathlib import Path

from bot.functions.crypt import decrypt_data
from bot.core.config import Config
from bot.core.logger import LOGS


def get_sessions(file_path=Config.SESSIONS_FILE):
    if not Path(file_path).exists():
        LOGS.error(f"File {file_path} does not exist")
        return

    with (open(file_path, "r") as json_file):
        encrypted_data = json.load(json_file)

        sessions = []
        key = Config.CRYPT_KEY
    for encrypted_session in encrypted_data.get("sessions", []):
        decrypted_session = decrypt_data(encrypted_session.encode('utf-8'), key)
        sessions.append(decrypted_session)

    return sessions