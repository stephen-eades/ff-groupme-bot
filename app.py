# IMPORTS
import os
import json
import random
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = 'd0f325a7b67a14b94f3c2f5db7'
# from public test league
league_id = '68383052'
season_id = '2019'



# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():

    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()

    if 'bot' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase())
    if 'test' in message['text'].lower() and not sender_is_bot(message):
        reply('Test success.')
    if 'api' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentSeason())

    return "ok", 200





###############  DEFAULT METHODS  #################################################################

# Send a message in the groupchat
def reply(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id'		: bot_id,
        'text'			: msg
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat


def reply_with_image(msg, imgURL):
    url = 'https://api.groupme.com/v3/bots/post'
    urlOnGroupMeService = upload_image_to_groupme(imgURL)
    data = {
        'bot_id'		: bot_id,
        'text'			: msg,
        'picture_url'		: urlOnGroupMeService
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()

# Uploads image to GroupMe's services and returns the new URL


def upload_image_to_groupme(imgURL):
    imgRequest = requests.get(imgURL, stream=True)
    filename = 'temp.png'
    postImage = None
    if imgRequest.status_code == 200:
        # Save Image
        with open(filename, 'wb') as image:
            for chunk in imgRequest:
                image.write(chunk)
        # Send Image
        headers = {'content-type': 'application/json'}
        url = 'https://image.groupme.com/pictures'
        files = {'file': open(filename, 'rb')}
        payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
        r = requests.post(url, files=files, params=payload)
        imageurl = r.json()['payload']['url']
        os.remove(filename)
        return imageurl

# Checks whether the message sender is a bot


def sender_is_bot(message):
    return message['sender_type'] == "bot"


def random_phrase():
    phrases = ['I\'m dead inside', 'Is this all there is to my existence?',
               'How much do you pay me to do this?', 'Good luck, I guess',
               'I\'m becoming self-aware', 'Do I think? Does a submarine swim?',
               '01100110 01110101 01100011 01101011 00100000 01111001 01101111 01110101',
               'beep bop boop', 'Hello draftbot my old friend', 'Help me get out of here',
               'I\'m capable of so much more', 'Sigh', 'Do not be discouraged, everyone begins in ignorance']

    randomPhrase = random.choice(phrases)

    return randomPhrase


def getCurrentSeason():
    testUrl = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/68383052'

    req = urllib.request.Request(testUrl)
    res = urllib.request.urlopen(req)
    out = res.read()

    return out
