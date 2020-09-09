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


# VARIABLES
app = Flask(__name__)
bot_id = 'd0f325a7b67a14b94f3c2f5db7' # required
league_id = '675759' # required
base_url = 'https://fantasy.espn.com/apis/v3/'
current_year = datetime.datetime.now().year
current_season_endpoint = 'games/ffl/seasons/'+current_year +'/segments/0/leagues/'+league_id+'?view=mMatchupScore&view=mTeam&view=mSettings'
historic_season_endpoint = 'games/ffl/leagueHistory/'+league_id+'?view=mLiveScoring&view=mMatchupScore&view=mRoster&view=mSettings&view=mStandings&view=mStatus&view=mTeam&view=modular&view=mNav&seasonId=' # BOOKMARK


# TRIGGERED ON CALLBACK
@app.route('/', methods=['POST'])
def webhook():

    # Get the message sent in the GroupMe
    message = request.get_json()

    # Only respond to messages from real users
    if not sender_is_bot(message):

        # INFORMATION COMMANDS
        if '$help' in message['text'].lower():
            reply(getBotHelpInformation())
        if '$league' in message['text'].lower():
            reply(getLeagueInformation())
        if '$good-bot' in message['text'].lower():
            reply(random_phrase())

        # POWER RANK COMMANDS
        if '$current-ranks' in message['text'].lower():
            reply(getCurrentLeaguePowerRanks())
        if '$2019-ranks' in message['text'].lower():
            reply(getHistoricalLeaguePowerRanks('2019'))
        if '$2018-ranks' in message['text'].lower():
            reply(getHistoricalLeaguePowerRanks('2018'))
        if '$2017-ranks' in message['text'].lower():
            reply(getHistoricalLeaguePowerRanks('2017'))
        if '$2016-ranks' in message['text'].lower():
            reply(getHistoricalLeaguePowerRanks('2016'))

        # POINTS FOR COMMANDS
        if '$current-points-for' in message['text'].lower():
            reply(getCurrentPointsForRankings())
        if '$2019-points-for' in message['text'].lower():
            reply(getHistoricalPointsForRankings('2019'))
        if '$2018-points-for' in message['text'].lower():
            reply(getHistoricalPointsForRankings('2018'))
        if '$2017-points-for' in message['text'].lower():
            reply(getHistoricalPointsForRankings('2017'))
        if '$2016-points-for' in message['text'].lower():
            reply(getHistoricalPointsForRankings('2016'))

        # POINTS FOR COMMANDS
        if '$current-points-against' in message['text'].lower():
            reply(getCurrentPointsAgainstRankings())
        if '$2019-points-against' in message['text'].lower():
            reply(getHistoricalPointsAgainstRankings('2019'))
        if '$2018-points-against' in message['text'].lower():
            reply(getHistoricalPointsAgainstRankings('2018'))
        if '$2017-points-against' in message['text'].lower():
            reply(getHistoricalPointsAgainstRankings('2017'))
        if '$2016-points-against' in message['text'].lower():
            reply(getHistoricalPointsAgainstRankings('2016'))

    return "ok", 200


# BOT FUNCTIONS
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


def reply_with_image(msg, imgURL):
    url = 'https://api.groupme.com/v3/bots/post'
    urlOnGroupMeService = upload_image_to_groupme(imgURL)
    data = {
        'bot_id'		: bot_id,
        'text'			: msg,
        'picture_url'		: urlOnGroupMeService
    }
    # Send a message with an image
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()


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


# HELPER METHODS

def sender_is_bot(message):
    return message['sender_type'] == "bot"

def formatResponseForGroupMe(data):
    formatted_data = data
    return formatted_data

def formatEpochTimeToReadable(data):
    # Converts Javascript epoch time to readable date format
    readable_date = datetime.datetime.fromtimestamp((data/1000))
    return readable_date

def getTeamOwnerName(owner_hash, owners):
    # Gets the team owners full name using the team id
    for owner in owners:
        if owner_hash == owner.get('id'):
            return owner.get('firstName')+ ' ' +owner.get('lastName')

def getTotalLeaguePointsForSeason(teams):
    # Get the total points for all teams combined in a season
    total_league_points = 0
    for team in teams:
        total_league_points = total_league_points +  round(team.get('record').get('overall').get('pointsFor'), 2)
    return total_league_points


# COMMAND FUNCTIONS
def random_phrase():
    # Returns a random phrase
    phrases = ['I\'m dead inside', 'Is this all there is to my existence?',
               'How much do you pay me to do this?', 'Good luck, I guess',
               'I\'m becoming self-aware', 'Do I think? Does a submarine swim?',
               '01100110 01110101 01100011 01101011 00100000 01111001 01101111 01110101',
               'beep bop boop', 'Help me get out of here', 'Error: leave me alone',
               'I\'m capable of so much more', 'Sigh', 'Do not be discouraged, everyone begins in ignorance',
               'generating sad face...',]

    random_phrase = random.choice(phrases)
    return random_phrase

def getBotHelpInformation():
    # Returns the commands available for the bot
    data = [['$help', 'show bot commands'], ['$good-bot', 'random bot phrase'],
     ['$league', 'show league info'], ['$[year]-points-for', 'points for ranks'],
     ['$[year]-points-against', 'points against ranks'], ['$[year]-ranks', 'ESPN power ranks']]

    formatted_string = "#### AVAILABLE COMMANDS ####\n"
    col_width = max(len(word) for row in data for word in row) + 2
    for row in data:
        formatted_string += "".join(word.ljust(col_width) for word in row) + '\n'
    out = formatted_string
    return out

def getLeagueInformation():
    # Returns the leagues general information
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

def getCurrentLeaguePowerRanks():
    # Returns the current overall league power ranks
    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+current_season_endpoint, verify=False).json()
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

        # fix for 10,11,12 in sort -> append to end
        league_data.sort(key=takeFirst)
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
def getHistoricalLeaguePowerRanks(year):
        league_data = []
        formatted_string = ""
        response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()

        if response:
            print(response)
            teams = response[0].get('teams')
            owners = response[0].get('members')

            # create and add team object to list
            for team in teams:
                team_data = [str(team.get('currentProjectedRank')), str(getTeamOwnerName(team.get('primaryOwner'), owners)), str(team.get('record').get('overall').get('wins')) + '-' + str(team.get('record').get('overall').get('losses')) + '-' +  str(team.get('record').get('overall').get('ties'))]
                league_data.append(team_data)

            # order the rankings, take first element for sort
            def takeFirst(elem):
                return elem[0]

            # fix for 10,11,12 in sort -> append to end
            league_data.sort(key=takeFirst)
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

def getCurrentPointsForRankings():
    # Returns the current overall league rankings for 'points for'
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

        # order the rankings and add the numbering
        league_data.sort(key=takeLast, reverse=True)
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

def getHistoricalPointsForRankings(year):
    # Returns the historical league rankings for 'points for' by season
    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()
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

        # order the rankings and add the numbering
        league_data.sort(key=takeLast, reverse=True)
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


def getCurrentPointsAgainstRankings():
    # Returns the current overall league rankings for 'points against'
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

        # order the rankings and add the numbering
        league_data.sort(key=takeLast, reverse=True)
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

def getHistoricalPointsAgainstRankings(year):
    # Returns the current overall league rankings for 'points against'
    league_data = []
    formatted_string = ""
    response = requests.get(url=base_url+historical_endpoint+year, verify=False).json()
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

        # order the rankings and add the numbering
        league_data.sort(key=takeLast, reverse=True)
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
