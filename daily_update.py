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
endpoint = 'games/ffl/seasons/2019/segments/0/leagues/'+league_id+'?view=mMatchupScore&view=mTeam&view=mSettings'

# TODO: Convert function names from mixedcase to python styling guide lower_case_names()

###############  MAIN  #################################################################

# Occurs when callback URL receives a POST request i.e. message sent in the group
@app.route('/', methods=['POST'])
def webhook():

    # Check the date and return league updates (note: 0 = Monday, 6 = Sunday)
    if datetime.datetime.today().weekday() == 1:
        reply(tuesday_score_update()) # send the final scores for the week Tuesday AM
    if datetime.datetime.today().weekday() == 0:
        reply(monday_close_games()) # send notice for tight matchups depending on MNF

    # TODO: Figure out specific day alerts
    # if datetime.datetime.today().weekday() == 1:
    #     reply(end_of_season_summary()) # display league stats for the season

    return "ok", 200


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


###############  SCHEDULED FUNCTIONS  ###########################################################

# Returns scores for the week
def tuesday_score_update():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        # if response.get('status').get('isActive') is True:
        #     currentWeek = response.get('status').get('currentMatchupPeriod')
        #     player_score_type = str(response.get('settings').get('scoringSettings').get('playerRankType'))

        # header = "#### WEEK ? ####\n"
        # first_line = league_name + " " + league_owner_count + " person " + player_score_type + " league \n"
        # second_line = 'League Founded: ' + league_creation_year + '\n'
        # third_line = 'Current Champion: Joshua Bailey \n'
        # fourth_line = 'Total League points: ' + str(getTotalLeaguePointsForSeason(response.get('teams')))

        # out = header + first_line + second_line + third_line + fourth_line
        out = ' Tuesday score update occurred with no error'
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out


# Returns matchups with tight scores depending on MNF
def tuesday_score_update():

    response = requests.get(url=base_url+endpoint, verify=False).json()

    if response:
        # league_name = response.get('settings').get('name')
        # player_score_type = str(response.get('settings').get('scoringSettings').get('playerRankType'))
        # league_creation_year = str(response.get('status').get('previousSeasons')[0])
        # league_owner_count = str(response.get('status').get('teamsJoined'))
        #
        # header = "#### LEAGUE INFO ####\n"
        # first_line = league_name + " " + league_owner_count + " person " + player_score_type + " league \n"
        # second_line = 'League Founded: ' + league_creation_year + '\n'
        # third_line = 'Current Champion: Joshua Bailey \n'
        # fourth_line = 'Total League points: ' + str(getTotalLeaguePointsForSeason(response.get('teams')))
        #
        # out = header + first_line + second_line + third_line + fourth_line
        out = ' Monday tight matchup occurred with no error'
    else:
        out = 'An error has occurred while retrieving from the API.'

    return out
