import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from requests_oauthlib import OAuth1Session
import requests
import traceback
import datetime
import time
import json
import sys

RETRY = 0

def browser(tweets):
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
        wait = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
        Alert(driver).accept()
        pyperclip.copy(json.dumps(b))
        actions = ActionChains(driver)
        actions.key_down(Keys.TAB)
        actions.key_down(Keys.TAB)
        actions.key_down(Keys.COMMAND)
        actions.send_keys('v').perform()
    
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
            sys.exit()
    else:
        driver.quit()
        print("End")
        sys.exit()


consumer_key = os.environ['CK']
consumer_secret = os.environ['CS']
access_token = os.environ['AT']
access_token_secret = os.environ['AS']
bearer_token = os.environ['BT']

oath = OAuth1Session(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def get_rules():
    response = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
    #print(json.dumps(response.json()))
    return response.json()

def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None
    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload)
    if response.status_code != 200:
        raise Exception("Cannot delete rules (HTTP {}): {}".format(response.status_code, response.text))
    #print(json.dumps(response.json()))

def set_rules(delete):
    rules = [{"value":"大阪"##[{"value":"\"334\" -is:retweet -is:reply -is:quote"}]
    payload = {"add": rules}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload)
    if response.status_code != 201:
        raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))
    #print(json.dumps(response.json()))

def get_stream(headers):
    global oath
    tweet_list = []
    now = datetime.datetime.now()
    start_time = datetime.datetime(now.year, now.month, now.day, 3, 34, 0)
    start_time = datetime.datetime(now.year, now.month, now.day, 2, 10, 0)
    end_time = datetime.datetime(now.year, now.month, now.day, 3, 34, 1)
    end_time = datetime.datetime(now.year, now.month, now.day, 2, 10, 1)
    send_time = datetime.datetime(now.year, now.month, now.day, 3, 34, 2)
    send_time = datetime.datetime(now.year, now.month, now.day, 2, 10, 2)
    send_flag = True
    run = 1
    while run:
        try:
            with requests.get("https://api.twitter.com/2/tweets/search/stream?tweet.fields=id,source,text&expansions=author_id&user.fields=id,name,profile_image_url,username", auth=bearer_oauth, stream=True) as response:
                if response.status_code != 200:
                    raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))
                for response_line in response.iter_lines():
                    if response_line:
                        json_response = json.loads(response_line)
                        epoch = ((int(json_response["data"]["id"]) >> 22) + 1288834974657) / 1000.0
                        d = datetime.datetime.fromtimestamp(epoch)
                        if tweet_text != "334":##########################
                            if start_time.time() <= d.time() < end_time.time():
                                tweet_text = json_response["data"]["text"]
                                diff = d - start_time
                                tweetdata = [
                                    json_response["includes"]["users"][0]["profile_image_url"],
                                    json_response["includes"]["users"][0]["name"],
                                    '{:.3f}'.format(diff.total_seconds()),
                                    json_response["data"]["source"],
                                    json_response["data"]["id"],
                                    json_response["includes"]["users"][0]["username"],
                                    json_response["data"]["author_id"]
                                ]
                                tweet_list.append(tweetdata)
							
                        if send_time.time() < d.time() and send_flag:
                            send_flag = False
                            tweet_list = sorted(tweet_list, reverse=True, key=lambda x: x[1])
                            browser(json.dumps(tweet_list))

        except ChunkedEncodingError as chunkError:
            print(traceback.format_exc())
            time.sleep(6)
            continue
        
        except ConnectionError as e:
            print(traceback.format_exc())
            run+=1
            if run <10:
                time.sleep(6)
                print("再接続します",run+"回目")
                continue
            else:
                run=0
        except Exception as e:
            # some other error occurred.. stop the loop
            print("Stopping loop because of un-handled error")
            print(traceback.format_exc())
            run = 0
	    
class ChunkedEncodingError(Exception):
    pass


rules = get_rules()
delete = delete_all_rules(rules)
set = set_rules(delete)
   
now = datetime.datetime.now()
start = datetime.datetime(now.year, now.month, now.day, 3, 33, 40, 0)
start = datetime.datetime(now.year, now.month, now.day, 2, 9, 40, 0)
now = datetime.datetime.now()
diff = start - now
print("Start sleep")
time.sleep(diff.total_seconds())

get_stream(set)

