# IMPORTS
import os
import json
import random
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
from pprint import pprint

app = Flask(__name__)
bot_id = 'd0f325a7b67a14b94f3c2f5db7'
league_id = '675759'
season_id = '2019'


###############  MAIN  #################################################################

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():

    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()

    if 'bot' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase())
    if 'public-league' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentSeasonPublic())
    return "ok", 200


###############  BOT METHODS  ###########################################################

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


# Returns a randomized robotic phrase
def random_phrase():
    phrases = ['I\'m dead inside', 'Is this all there is to my existence?',
               'How much do you pay me to do this?', 'Good luck, I guess',
               'I\'m becoming self-aware', 'Do I think? Does a submarine swim?',
               '01100110 01110101 01100011 01101011 00100000 01111001 01101111 01110101',
               'beep bop boop', 'Hello draftbot my old friend', 'Help me get out of here',
               'I\'m capable of so much more', 'Sigh', 'Do not be discouraged, everyone begins in ignorance']

    randomPhrase = random.choice(phrases)

    return randomPhrase


###############  FF METHODS  ###########################################################

# TODO:
# Fix SSL CA Cert error via https://stackoverflow.com/a/51408997 => #3. This is currently worked around with verify=False for dev
# Work on getting from public league and formatting data. Build out functions set to execute based on day of week/time

def getCurrentSeasonPublic():

    base = 'https://fantasy.espn.com/apis/v3/'
    public_currentSeason = base + 'games/ffl/seasons/2019/segments/0/leagues/675759'

    response = requests.get(url=public_currentSeason, verify=False)

    if response:
        out = str(response.text)
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# def getCurrentSeasonPrivate():
#
#     league_id = 675759
#     year = 2018
#     url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
#           str(league_id) + "?seasonId=" + str(year)
#
#     cookies={"swid": "{DEB2F8EB-E1D5-49DD-B195-0B34463F4664}", "espn_s2": "AEBLvEKLkqVOa2jgOXhyzYbyrnU0yAlPOR1Ple4ndSmLsiLyIZHBOeO0hraZ2MH5bFOVbfGTcuOwWc3A9YVY25KUVN3hAuMeIebsJdaTPQWPHe%2BAASgiDbA739AkyWmlKVV06Cp4J1PLdShobIrVPFJkASNQM%2Fs3wsdIeU7pJmuzSeHlVzwVoUHZiDM3hq85uH%2FKrJ%2BmmzMnUKAIGyd5GuZrJGEVtVrVupLqcAERUbDH0Fv3BTD29RtKbmpxA5RsqWpQrtkKlbY1%2BhQ1oaYCn6JlsFmTNszhBZQsb4c5uwj4RA%3D%3D"}
#
#     response = requests.get(url=url, cookies=cookies, verify=False)
#
#     if response:
#         out = response
#     else:
#         out = 'An error has occurred while retrieving from the API.'
#
#     return out


# def getCurrentSeasonPrivateText():
#
#     league_id = 675759
#     year = 2018
#     url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
#           str(league_id) + "?seasonId=" + str(year)
#
#     cookies={"swid": "{DEB2F8EB-E1D5-49DD-B195-0B34463F4664}", "espn_s2": "AEBLvEKLkqVOa2jgOXhyzYbyrnU0yAlPOR1Ple4ndSmLsiLyIZHBOeO0hraZ2MH5bFOVbfGTcuOwWc3A9YVY25KUVN3hAuMeIebsJdaTPQWPHe%2BAASgiDbA739AkyWmlKVV06Cp4J1PLdShobIrVPFJkASNQM%2Fs3wsdIeU7pJmuzSeHlVzwVoUHZiDM3hq85uH%2FKrJ%2BmmzMnUKAIGyd5GuZrJGEVtVrVupLqcAERUbDH0Fv3BTD29RtKbmpxA5RsqWpQrtkKlbY1%2BhQ1oaYCn6JlsFmTNszhBZQsb4c5uwj4RA%3D%3D"}
#
#     response = requests.get(url=url, cookies=cookies, verify=False)
#
#     if response:
#         out = response.text
#     else:
#         out = 'An error has occurred while retrieving from the API.'
#
#     return out
