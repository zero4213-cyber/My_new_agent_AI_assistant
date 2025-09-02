# security/encryption.py - mã hóa tệp tin

import os
import logging
from cryptography.fernet import Fernet

from utils.error_logger import learn_from_failure

def encrypt_file(file_path, key=None):
    """Mã hóa file bằng Fernet symmetric encryption."""
    try:
        if not key:
            key = Fernet.generate_key()
        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        encrypted_path = file_path + ".enc"
        with open(encrypted_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        return encrypted_path, key
    except Exception as e:
        logging.error(f"Lỗi khi mã hóa file: {e}")
        learn_from_failure("encrypt_file", e)
        return "", None