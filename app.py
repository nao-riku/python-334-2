import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import datetime
import time

RETRY = 0

def browser():
    print("Start Browsing")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(620, 1)
    driver.get(os.environ['URL']) 
    time.sleep(3)
    driver.quit()
    print("End")
    
now = datetime.datetime.today()
if 27 < now.minute < 30:
    print("yet")
else:
    browser()
