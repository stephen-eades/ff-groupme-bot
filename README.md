# Boilerplate GroupMe Bot *(Python 3)*

The humble beginnings for *your* shiny new GroupMe bot! This boilerplate draws heavily on @apnorton's example, which he discusses in depth in his blogpost, ["How I wrote a GroupMe Chatbot in 24 hours"](http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/). I've added a few functions to abstract away common needs.

## Setup & Deployment

This bot boilerplate is written in Python 3, and is designed to be deployed on Heroku servers. To start developing using this boilerplate...

1. [Install Python 3](https://www.python.org/downloads/)

2. [Create a Heroku account](https://signup.heroku.com/)

3. [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) -- I recommend using the default settings.

4. In a Git-enabled terminal, clone this repository.

	- That command is `git clone git@github.com:BenDMyers/Boilerplate_GroupMe_Bot.git`

5. In your newly Heroku-enabled terminal, navigate into the repository you just cloned.

6. Log in to the Heroku CLI by calling `heroku login`

	- When prompted, give the same credentials you used for your Heroku account.

7. Initialize the Heroku app by calling `heroku create your-app-name`

	- Heroku requires every app it hosts to have a totally unique name

8. Updates to your app are sent through Git, but this requires Git to know which remote repository to push to. To set the remote repository, call `heroku git:remote -a your-app-name`

9. The repository is now linked to a new Heroku app. To deploy a new version of your app at any time, just use Git.

	1. `git add .` to queue modified files to be committed

	2. `git commit -m "Description of changes here"` to save a snapshot of the codebase

	3. `git push heroku master` to send that snapshot to Heroku

		- This will automatically cause Heroku to redeploy your app with the changes.

	4. To view your app's logs while it is deployed, call `heroku logs`. This will show the past hundred lines of logs.

		- I've found `heroku logs -t` to be more useful. It will pull up the past hundred lines, but then it will show new log messages in real time.

10. ***Only do this when you're sure your bot is [ready to go live](https://i.memecaptain.com/gend_images/Zi5JCA.jpg) so you don't annoy those in the groupchat with your testing. Instead of testing with `reply()`, test by `print()`-ing to the Heroku logs.*** To add your bot to a GroupMe groupchat...

	1. Go to [dev.groupme.com/bots](https://dev.groupme.com/bots) and click 'Create bot'.

	2. Choose which group this bot will belong to, and give the bot a name and an avatar. The callback URL **must** be `https://your-app-name.herokuapp.com/`. This specifies that every message in the groupchat should be sent as a JSON `POST` request to your app.

	3. Copy the bot ID that GroupMe gives you, and set the `bot_id` variable in `app.py` to this ID. Redeploy. This way, your bot can send messages to the groupchat.

#### `Procfile`

[Heroku's Procfile docs](https://devcenter.heroku.com/articles/procfile) | [Heroku's Procfile+Gunicorn docs](https://devcenter.heroku.com/articles/python-gunicorn)

The Procfile is a text file named `Procfile` exactly, placed in the app's root directory. The Procfile determines which commands Heroku's dynos should run. The boilerplate Procfile looks like

```
web: gunicorn app:app --log-file=-
```

Here, the Procfile tells Heroku to spin up a Gunicorn Python webserver. It's taking the `app` variable (first `app`), which is a Flask application, from the `app.py` module (second `app`), and running it as a `web` process. The `--log-file=-` tells Heroku to log error messages to stdout, i.e. `heroku logs`.

#### `requirements.txt`

This lets Heroku know which Python package dependencies to install for this app, and which versions. The boilerplate specifies that Flask and Gunicorn, both used here to serve up a webapp, are required.

#### `runtime.txt`

When you include `requirements.txt`, Heroku can infer that you're deploying a Python app, but it can't determine whether to use Python 2 or 3, or which specific version to use. This boilerplate currently specifies `python-3.6.2`, but Heroku lets you specify any version up to the latest stable releases of Python 2 and 3.

#### `app.py`

The bot code itself. With `app = Flask(__name__)`, a Flask application is created. Every time a message is sent in a groupchat, GroupMe will send the message as a `POST` request to the chat's bots' callback URLs. To catch this on the app end, we use some Flask routing.

```python
@app.route('/', methods=['POST'])
```

This means the following function, `webhook()`, will be called every time the homepage of the callback site receives a `POST` request. Because of this, you can think of `webhook()` as the bot's main method whenever it receives any message.

The other functions, which follow the line of pound signs, are just there to make common tasks simpler.