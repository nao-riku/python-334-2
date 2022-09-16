import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sched
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
    try:
        wait = WebDriverWait(driver, 30)
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
        
    
now = datetime.datetime.datetime.now()
start = datetime.datetime(now.year, now.month, now.day, now.hour, 41)
diff = start - now

print("Set Sched")
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(diff.seconds, 1, browser)
scheduler.run()
