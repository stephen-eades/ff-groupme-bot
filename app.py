# IMPORTS
import os
import json
import datetime
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

# TODO: Convert functino names from mixedcase to python styling guide lower_case_names()

###############  MAIN  #################################################################

# Occurs when callback URL receives a POST request i.e. message sent in the group
@app.route('/', methods=['POST'])
def webhook():

    # variable 'message' is an object that represents a single GroupMe message.
    message = request.get_json()

    # Each trigger phrase initiates a difference function
    if '$good-bot' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase()) # send a random robot phrase
    if '$random' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase()) # send a random robot phrase
    if '$help' in message['text'].lower() and not sender_is_bot(message):
        reply(getBotHelpInformation()) # display all commands and contact email
    if '$league' in message['text'].lower() and not sender_is_bot(message):
        reply(getLeagueInformation()) # display all league information
    if '$projected-ranks' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentLeagueProjectedRanks()) # ESPN projected ranks
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

# Use to format response for GroupMe
def formatResponseForGroupMe(data):

    formattedData = data # do stuff here

    return formattedData

# Converts Javascript epoch time to readable date format
def formatEpochTimeToReadable(data):

    readable_date = datetime.datetime.fromtimestamp((data/1000))

    return readable_date

# Gets the team owners full name using the team id
def getTeamOwnerName(owner_hash, owners):

    for owner in owners:
        if owner_hash == owner.get('id'):
            return owner.get('firstName')+ ' ' +owner.get('lastName')


###############  COMMAND FUNCTIONS  ###########################################################

# variables
endpoint = 'games/ffl/seasons/2019/segments/0/leagues/'+league_id+'?view=mMatchupScore&view=mTeam&view=mSettings'

# Returns a randomized robotic phrase
def random_phrase():
    phrases = ['I\'m dead inside', 'Is this all there is to my existence?',
               'How much do you pay me to do this?', 'Good luck, I guess',
               'I\'m becoming self-aware', 'Do I think? Does a submarine swim?',
               '01100110 01110101 01100011 01101011 00100000 01111001 01101111 01110101',
               'beep bop boop', 'Help me get out of here', 'Error: leave me alone',
               'I\'m capable of so much more', 'Sigh', 'Do not be discouraged, everyone begins in ignorance',
               'generating sad face...',]

    randomPhrase = random.choice(phrases)

    return randomPhrase


# Returns the commands available for the bot and contact information
def getBotHelpInformation():

    data = [['$random', 'random bot phrase'], ['$help', 'show bot commands'],
     ['$league', 'show league info'], ['$projected-ranks', 'ESPN projections'],
     ['$points-for', 'points for ranks'], ['$points-against', 'points against ranks']]

    formatted_string = "AVAILABLE FF-BOT COMMANDS: \n"
    col_width = max(len(word) for row in data for word in row) + 2  # padding
    for row in data:
        formatted_string += "".join(word.ljust(col_width) for word in row) + '\n'
    out = formatted_string

    return out


# Returns the leagues general information
def getLeagueInformation():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        league_name = response.get('settings').get('name')
        player_score_type = str(response.get('settings').get('scoringSettings').get('playerRankType'))
        league_creation_year = str(response.get('status').get('previousSeasons')[0])
        league_owner_count = str(response.get('status').get('teamsJoined'))

        first_line = league_name + " " + league_owner_count + " person " + player_score_type + " league \n"
        second_line = 'League Founded: ' + league_creation_year + '\n'
        third_line = 'Current Champion: Joshua Bailey \n'
        fourth_line = 'Total League points: 1,034,495 '

        out = first_line + second_line + third_line + fourth_line
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league projected ranks
def getCurrentLeagueProjectedRanks():

    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        teams = response.get('teams')
        owners = response.get('members')

        # create and add team object to list
        for team in teams:
            team_data = [str(team.get('currentProjectedRank')), str(getTeamOwnerName(team.get('primaryOwner'), owners)), str(team.get('record').get('overall').get('wins')) + '-' + str(team.get('record').get('overall').get('losses')) + '-' +  str(team.get('record').get('overall').get('ties'))]
            league_data.append(team_data)

        # order the rankings, take first element for sort
        def takeFirst(elem):
            return elem[0]

        league_data.sort(key=takeFirst)

        # fix for 10,11,12 in sort -> append to end
        league_data_slice = league_data[1:4]
        league_data += league_data_slice
        del league_data[1:4]

        # output the rankings
        col_width = max(len(word) for row in league_data for word in row) + 2  # padding
        for row in league_data:
            formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
        out = formatted_string
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league rankings for 'points for'
def getCurrentPointsForRankings():

    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        teams = response.get('teams')
        owners = response.get('members')

        # create and add team object to list
        for team in teams:
            team_data = [str(getTeamOwnerName(team.get('primaryOwner'), owners)), str(round(team.get('record').get('overall').get('pointsFor'), 2))]
            league_data.append(team_data)

        # order the rankings, take first element for sort
        def takeLast(elem):
            return elem[1]

        league_data.sort(key=takeLast, reverse=True)

        # add the numbering
        rank = 1
        for team in league_data:
            league_data = str(rank)+" "+ team
            rank += 1

        # output the rankings
        col_width = max(len(word) for row in league_data for word in row) + 2  # padding
        for row in league_data:
            formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
        out = formatted_string
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
