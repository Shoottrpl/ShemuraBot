import json
import os.path

from pathlib import Path
from bot.core.logger import LOGS
from bot.core.config import Config
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet

root = Config.ROOT

dotenv_path = os.path.join(root, ".env")
load_dotenv(dotenv_path)


def generate_key() -> bytes:
    key =  Fernet.generate_key()
    set_key(dotenv_path, "CRYPT_KEY", key.decode())
    LOGS.info(f"New key success save in {root}")
    return key

def encrypt_data(data: str, key: str) -> bytes:
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode("utf-8"))
    return encrypted_data

def decrypt_data(encrypted_data: bytes, key: str) -> json:
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
    return decrypted_data

def save_encrypted_data(encrypted_data: bytes, file_path: str, index=None) -> None:
    if Path(file_path).exists():
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        data = {}

    if index not in data:
        data[index] = []

    data[index].append(encrypted_data.decode("utf-8"))

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)



