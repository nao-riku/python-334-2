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
    
now = datetime.datetime.today()
if 27 < now.minute < 30:
    print("yet")
else:
    browser()
