import os
from fastapi import FastAPI
from fastapi import BackgroundTasks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import datetime
import time

app = FastAPI()

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
    try:
        wait = WebDriverWait(driver, 50)
        wait.until(expected_conditions.alert_is_present())
    except Exception as e:
        driver.quit()
        print("Err")
        print(e)
        global RETRY
        if RETRY < 4:
            time.sleep(5)
            RETRY += 1
            browser()
        else:
            print("AllErr")
    else:
        driver.quit()
        print("End")

@app.get('/')
async def main(background_tasks: BackgroundTasks):
    now = datetime.datetime.today()
    if 27 < now.minute < 30:
        return "yet"
    else:
        background_tasks.add_task(browser)
        print("Response")
        return "OK"
