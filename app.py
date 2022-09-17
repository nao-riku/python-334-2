import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from requests_oauthlib import OAuth1Session
import requests
import datetime
import time

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
    rules = [{"value":"\"334\" -is:retweet -is:reply -is:quote"}]
    payload = {"add": rules}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload)
    if response.status_code != 201:
        raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))
    #print(json.dumps(response.json()))

def get_stream(headers):
    global oath
    run = 1
    start = time.time()
    while run:
        try:
            with requests.get("https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True) as response:
                if response.status_code != 200:
                    raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))
                for response_line in response.iter_lines():
                    if response_line:
                        json_response = json.loads(response_line)
                        tweet_text = json_response["data"]["text"]
                        if "@Rank334" in tweet_text or "@rank334" in tweet_text:
                            reply_id = json_response["data"]["id"]
                            rep_text = ""
						
                            if 'referenced_tweets' in json_response["data"]:
                                if json_response["data"]['referenced_tweets'][0]["type"] == "retweeted":
                                    continue
                                else:
                                    tweet_id = json_response["data"]['referenced_tweets'][0]["id"]
                                    rep_text = "ツイート時刻: " + TweetId2Time(int(tweet_id))
                            else:
                                rep_text = "ツイート時刻: " + TweetId2Time(int(reply_id)) + "\n\n順位: /"
							
                            print(rep_text)
                            params = {"text": rep_text, "reply": {"in_reply_to_tweet_id": reply_id}}
                            response = oath.post("https://api.twitter.com/2/tweets", json = params)
                            print(response.headers["x-rate-limit-remaining"])
                            if "status" in response.json():
                                if response.json()["status"] == 429:
                                    response = oath.post("https://api.twitter.com/2/tweets", json = params, proxies = proxy_dict)
							
                            if time.time() - start > 40:
                                sys.exit()


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
        
    
now = datetime.datetime.now()
print(now)
start = datetime.datetime(now.year, now.month, now.day, now.hour, 33, 50, 0)
print(start)
diff = start - now
print("Start sleep")
time.sleep(diff.total_seconds())

