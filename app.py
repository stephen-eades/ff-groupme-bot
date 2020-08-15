# IMPORTS
import os
import json
import datetime
import random
import requests
import schedule
import time
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
    # Send a random robot phrase
    if '$good-bot' in message['text'].lower() or '$random' in message['text'].lower() and not sender_is_bot(message):
        reply(random_phrase())

    # Display all commands and contact email
    if '$help' in message['text'].lower() and not sender_is_bot(message):
        reply(getBotHelpInformation())

    # Display all league information
    if '$league' in message['text'].lower() and not sender_is_bot(message):
        reply(getLeagueInformation())

    # ESPN power ranks
    if '$power-ranks' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentLeaguePowerRanks())
    if '$power-ranks-2019' in message['text'].lower() and not sender_is_bot(message):
        reply(get2019LeaguePowerRanks())
    if '$power-ranks-2018' in message['text'].lower() and not sender_is_bot(message):
        reply(get2018LeaguePowerRanks())
    if '$power-ranks-2017' in message['text'].lower() and not sender_is_bot(message):
        reply(get2017LeaguePowerRanks())


    # league rankings for 'points for'
    if '$points-for' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentPointsForRankings())

    # league rankings for 'points against'
    if '$points-against' in message['text'].lower() and not sender_is_bot(message):
        reply(getCurrentPointsAgainstRankings())



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

# Gets the total points for all teams in a season
def getTotalLeaguePointsForSeason(teams):
    total_league_points = 0

    for team in teams:
        total_league_points = total_league_points +  round(team.get('record').get('overall').get('pointsFor'), 2)
    return total_league_points


###############  COMMAND FUNCTIONS  ###########################################################

# variables
endpoint = 'games/ffl/seasons/2019/segments/0/leagues/'+league_id+'?view=mMatchupScore&view=mTeam&view=mSettings'
historical_endpoint = 'games/ffl/leagueHistory/'+league_id+'?view=mLiveScoring&view=mMatchupScore&view=mRoster&view=mSettings&view=mStandings&view=mStatus&view=mTeam&view=modular&view=mNav&seasonId='

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

    data = [['$help', 'show bot commands'], ['$random', 'random bot phrase'],
     ['$league', 'show league info'], ['$points-for', 'points for ranks'],
     ['$points-against', 'points against ranks'], ['$power-ranks', 'ESPN power ranks']]

    formatted_string = "#### AVAILABLE COMMANDS ####\n"
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

        header = "#### LEAGUE INFO ####\n"
        first_line = league_name + " " + league_owner_count + " person " + player_score_type + " league \n"
        second_line = 'League Founded: ' + league_creation_year + '\n'
        third_line = 'Current Champion: Joshua Bailey \n'
        fourth_line = 'Total League points: ' + str(getTotalLeaguePointsForSeason(response.get('teams')))

        out = header + first_line + second_line + third_line + fourth_line
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league power ranks
def getCurrentLeaguePowerRanks():

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
        formatted_string = "#### POWER RANKINGS ####\n"
        col_width = max(len(word) for row in league_data for word in row) + 2  # padding
        for row in league_data:
            formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
        out = formatted_string
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league power ranks
def get2019LeaguePowerRanks():

        year = '2019'

        league_data = []
        formatted_string = ""
        response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()

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
            formatted_string = "#### 2019 POWER RANKINGS ####\n"
            col_width = max(len(word) for row in league_data for word in row) + 2  # padding
            for row in league_data:
                formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
            out = formatted_string
        else:
            out = 'An error has occurred while retrieving from the API.'

        return out

# Returns the current overall league power ranks
def get2018LeaguePowerRanks():

        year = '2018'

        league_data = []
        formatted_string = ""
        response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()

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
            formatted_string = "#### 2018 POWER RANKINGS ####\n"
            col_width = max(len(word) for row in league_data for word in row) + 2  # padding
            for row in league_data:
                formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
            out = formatted_string
        else:
            out = 'An error has occurred while retrieving from the API.'

        return out


# Returns the current overall league power ranks
def get2017LeaguePowerRanks():

        year = '2017'

        league_data = []
        formatted_string = ""
        response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()

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
            formatted_string = "#### 2017 POWER RANKINGS ####\n"
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

        # take first element for sort
        def takeLast(elem):
            return elem[1]

        # order the rankings
        league_data.sort(key=takeLast, reverse=True)

        # add the numbering
        rank = 1
        for team in league_data:
            team.insert(0, str(rank))
            rank += 1

        # output the rankings
        formatted_string = "#### POINTS FOR ####\n"
        col_width = max(len(word) for row in league_data for word in row) + 2  # padding
        for row in league_data:
            formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
        out = formatted_string
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns the current overall league rankings for 'points against'
def getCurrentPointsAgainstRankings():

    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        teams = response.get('teams')
        owners = response.get('members')

        # create and add team object to list
        for team in teams:
            team_data = [str(getTeamOwnerName(team.get('primaryOwner'), owners)), str(round(team.get('record').get('overall').get('pointsAgainst'), 2))]
            league_data.append(team_data)

        # take first element for sort
        def takeLast(elem):
            return elem[1]

        # order the rankings
        league_data.sort(key=takeLast, reverse=True)

        # add the numbering
        rank = 1
        for team in league_data:
            team.insert(0, str(rank))
            rank += 1

        # output the rankings
        formatted_string = "#### POINTS AGAINST ####\n"
        col_width = max(len(word) for row in league_data for word in row) + 2  # padding
        for row in league_data:
            formatted_string += "".join(word.ljust(col_width) for word in row) + '\n' # this outputs the row
        out = formatted_string
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out
