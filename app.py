# IMPORTS
import os
import json
import random
import requests
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
    if 'public' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentSeasonPublic())
    if 'private' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentSeasonPrivate())
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


def getCurrentSeasonPublic():

    base = 'https://fantasy.espn.com/apis/v3/'
    public_2017Season = base + 'games/ffl/leagueHistory/68383052?seasonId=2017'
    public_currentSeason = base + 'games/ffl/seasons/2019/segments/0/leagues/68383052'

    response = requests.get(url=public_currentSeason, verify=False)

    if response:
        # out = response
        out = response.text
        # out = response.content
        # out = response.json()
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


def get2017SeasonPublic():

    base = 'https://fantasy.espn.com/apis/v3/'
    public_2017Season = base + 'games/ffl/leagueHistory/68383052?seasonId=2017'

    response = requests.get(url=public_2017Season, verify=False)

    if response:
        # out = response
        out = response.text
        # out = response.content
        # out = response.json()
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


def getCurrentSeasonPrivate():

    base = 'https://fantasy.espn.com/apis/v3/'
    private_2017Season = base + 'games/ffl/leagueHistory/675759?seasonId=2017'
    private_currentSeason = base + 'games/ffl/seasons/2019/segments/0/leagues/675759'
    cookies={"swid": "{DEB2F8EB-E1D5-49DD-B195-0B34463F4664}", "espn_s2": "AEADnnU1FkNM%2FCzvBl%2Fv6I2IKmZc8bwT1DLhPnRui%2Fykw2eGcKRJ%2ByoGYrdwdAsBf%2B%2Byig2tQyCwgCBGsYbzSu9L2Bj7rTmFIp79GWaTah0nkCQvQ8Shv0IUZfEJPCeqtmEEnGcEbwD9wdLSmZ3D10pJXL35%2FIp8X1Y55MHTkQ3Or%2F5Y1ccoOz1NTPNtfIBkq2PLK2cHnWRd9wh5%2FUsudry6Ul2a9d6K1L09q3BxIvfVgirsKZPuvDM17TGI%2Bfh89yac1wnURXFoaeHL%2FynaJupaeI1%2BUnWih2jG3JCy0eFWbw%3D%3D"}

    response = requests.get(url=private_currentSeason, cookies=cookies, verify=False)

    if response:
        # out = response
        out = response.text
        # out = response.content
        # out = response.json()
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out
