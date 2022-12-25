import random
import string

def random_account():
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    email = "".join([random.choice(alphabet) for _ in range(random.randint(8, 15))]) + "@gmail.com"
    password = "".join([random.choice(alphabet) for _ in range(random.randint(8, 12))])
    return f"{email}:{password}"

with open('accounts.txt', 'a') as file:
    for _ in range(50):
        rdm_acc = random_account()
        print(rdm_acc)
        file.write(rdm_acc + "\n")

