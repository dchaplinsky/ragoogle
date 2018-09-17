import re

def is_eng(name):
    return re.search("[a-z]+", name.lower(), re.UNICODE) is not None
