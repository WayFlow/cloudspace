import hashlib
import time
import uuid
import zlib


def generate_secret_key():
    app_id = str(uuid.uuid4())
    current_time = str(int(time.time()))
    combined_string = app_id + current_time
    secret_key = hashlib.md5(combined_string.encode()).hexdigest()
    return secret_key


def generate_crc32_hash(value : str) -> str:
    crc32_hash = zlib.crc32(value.encode())
    return format(crc32_hash, '08x')
