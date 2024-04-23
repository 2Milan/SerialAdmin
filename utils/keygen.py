import string
import random

def generate_key(length: int) -> str:
    c1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    c2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    c3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    c4 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return c1 + '-' + c2 + '-' + c3 + '-' + c4