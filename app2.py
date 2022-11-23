import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from requests_oauthlib import OAuth1Session
import chromedriver_binary
import pyperclip
import requests
import traceback
import datetime
import time
import json
import sys

RETRY = 0

def browser(tweets):
    print("Start Browsing")
    global RETRY
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
        wait = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
        Alert(driver).accept()
        pyperclip.copy(tweets)
        actions = ActionChains(driver)
        actions.key_down(Keys.TAB)
        actions.key_down(Keys.TAB)
        actions.key_down(Keys.COMMAND)
        actions.send_keys('v').perform()
        wait2 = WebDriverWait(driver, 60).until(expected_conditions.alert_is_present())
    except Exception as e:
        driver.quit()
        print("Err")
        print(e)
        if RETRY < 5:
            time.sleep(5)
            RETRY += 1
            browser(tweets)
        else:
            print("AllErr")
            sys.exit()
    else:
        driver.quit()
        print("End")
        time.sleep(60)
        RETRY = 0
        browser2()
        

def browser2():
    print("Start Browsing2")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(620, 1)
    driver.get(os.environ['URL'] + "?p=month")
    
    try:
        wait = WebDriverWait(driver, 120).until(expected_conditions.alert_is_present())
    except Exception as e:
        driver.quit()
        print("Err")
        print(e)
        global RETRY
        if RETRY < 5:
            time.sleep(5)
            RETRY += 1
            browser2()
        else:
            print("AllErr")
            sys.exit()
    else:
        driver.quit()
        print("End")
        sys.exit()
        
browser("[]")
