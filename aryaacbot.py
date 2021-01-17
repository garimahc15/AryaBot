import chat_decision 
import json
import requests
import time
import urllib

TOKEN = "1456898905:AAFxIy8Lf7GX5T_MMGIhmj7mKG4CwsXVRe4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)   #downloads the content from url passed in argument
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)  #Telegram gives us JSON response. load string (loads) into a python dictionary
    return js

def get_updates(offset=None):
    #calls API command & will retrieve a list of updates (messages sent to our Bot)
    url = URL + "getUpdates?timeout=100"
    if offset:
        #If this is specified, we'll pass it along to the Telegram API to indicate that we
        # don't want to receive any messages with smaller IDs than this.
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids= []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
        return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)  #encode any special characters in our message
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def make_bot_resp(user_resp, first_name):
    if user_resp is not None:
        bot_resp = chat_decision.bot_response(user_resp, first_name)
    return bot_resp


def call_arya(updates):
    for update in updates["result"]:
        try:
            user_resp = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            first_name = update["message"]["chat"]["first_name"]
            bot_resp = make_bot_resp(user_resp, first_name)
            send_message(bot_resp, chat_id)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:  #if there are new updates
            last_update_id = get_last_update_id(updates) + 1
            call_arya(updates)
        #to get the most recent messages from Telegram every half second.
        time.sleep(0.5)

if __name__ == '__main__':
    main()