import random
import string

##Ordercodes are generated as soon as the Order form is submitted.

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_order_code():
    random_string = get_random_string(4)
    random_digit = str(random.randint(88888,99999))
    order_code = random_digit + "_" + random_string
    return order_code