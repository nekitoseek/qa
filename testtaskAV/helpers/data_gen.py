import random
import string

def random_seller_id():
    return random.randint(111111, 999999)

def random_name(n=8):
    return "test" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def random_price():
    return random.randint(1, 100000)