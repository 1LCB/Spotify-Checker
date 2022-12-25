import random
import string

def random_account():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    user = "".join([random.choice(letters) for _ in range(random.randint(8, 15))])
    password = "".join([random.choice(string.digits) for _ in range(random.randint(6, 10))])
    return f"{user}:{password}"

with open('accounts.txt', 'a') as file:
    for _ in range(50):
        file.write(random_account() + "\n")
