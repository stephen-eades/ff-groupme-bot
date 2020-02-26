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
bot_id = 'd0f325a7b67a14b94f3c2f5db7' # required
league_id = '675759' # required
base_url = 'https://fantasy.espn.com/apis/v3/'


###############  MAIN  #################################################################

# Occurs when callback URL receives a POST request i.e. message sent in the group
@app.route('/', methods=['POST'])
def webhook():

    # variable 'message' is an object that represents a single GroupMe message.
    message = request.get_json()

    # Each trigger phrase initiates a difference function
    if '$random' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase()) # send a random robot phrase
    if '$help' in message['text'].lower() and not sender_is_bot(message):
        reply(getBotHelpInformation()) # display all commands and contact email
    if '$league' in message['text'].lower() and not sender_is_bot(message):
        reply(getLeagueInformation()) # display all league information
    if '$standings' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentLeagueStandings()) # current overall league standings
    if '$points-for' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentPointsForRankings()) # league rankings for 'points for'
    if '$points-against' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentPointsAgainstRankings()) # league rankings for 'points against'

    return "ok", 200



###############  BOT-REPLY FUNCTIONS  ###########################################################

# Send a message in the groupchat
def reply(msg):

    url = 'https://api.groupme.com/v3/bots/post'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36' }
    data = {
        'bot_id'		: bot_id,
        'text'			: msg,
        'headers'       : headers
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



###############  HELPER METHODS  ########################################################

def formatResponseForGroupMe(data):
    formattedData = data
    return formattedData



###############  COMMAND FUNCTIONS  ###########################################################

# variables
endpoint = 'games/ffl/seasons/2019/segments/0/leagues/'+league_id+'?view=mMatchupScore&view=mTeam&view=mSettings'

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


# Returns the commands available for the bot and contact information
def getBotHelpInformation():

    data = [['$random', 'random bot phrase'], ['$help', 'show bot commands'],
     ['$league', 'show league info'], ['$standings', 'current standings'],
     ['$points-for', 'points for ranks'], ['$points-against', 'points against ranks']]

    formatted_string = "AVAILABLE FF-BOT COMMANDS: \n"
    col_width = max(len(word) for row in data for word in row) + 2  # padding
    for row in data:
        formatted_string += "".join(word.ljust(col_width) for word in row) + '\n'
    out = formatted_string

    print(formatted_string)
    return out


# Returns the leagues general information
def getLeagueInformation():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        out = response.get('members')[random.randrange(0, 12, 1)].get('lastName')
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league standings
def getCurrentLeagueStandings():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        out = response.get('members')[random.randrange(0, 12, 1)].get('lastName')
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league rankings for 'points for'
def getCurrentPointsForRankings():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        out = response.get('members')[random.randrange(0, 12, 1)].get('lastName')
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league rankings for 'points for'
def getCurrentPointsAgainstRankings():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        out = response.get('members')[random.randrange(0, 12, 1)].get('lastName')
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out



    ###############  SCHEDULED FUNCTIONS  ###########################################################
