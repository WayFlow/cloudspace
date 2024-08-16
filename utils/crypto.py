import hashlib
import time

def generate_secret_key(app_id):
    current_time = str(int(time.time()))
    combined_string = app_id + current_time
    secret_key = hashlib.md5(combined_string.encode()).hexdigest()
    return secret_key
