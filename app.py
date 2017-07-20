# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = ""

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route ('/', methods=['POST'])
def webhook():
	data = request.get_json()
	# 'data' is an object 
	return "ok", 200

def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id' : bot_id,
		'text'   : msg,
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()