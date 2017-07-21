# Boilerplate GroupMe Bot *(Python 3)*

The humble beginnings for *your* shiny new GroupMe bot! This boilerplate draws heavily on @apnorton's example, which he discusses in depth in his blogpost, ["How I wrote a GroupMe Chatbot in 24 hours"](http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/). I've added a few functions to abstract away common needs.

## Setup

This bot boilerplate is written in Python 3, and is designed to be deployed on Heroku servers. To start developing using this boilerplate...

1. [Install Python 3](https://www.python.org/downloads/)

2. [Create a Heroku account](https://signup.heroku.com/)

3. [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

4. In a Git-enabled terminal, clone this repository.

	- That command is `git clone git@github.com:BenDMyers/Boilerplate_GroupMe_Bot.git`

5. In your newly Heroku-enabled terminal, navigate into the repository you just cloned.

6. Log in to the Heroku CLI by calling `heroku login`

	- When prompted, give the same credentials you used for your Heroku account.

7. Initialize the Heroku app by calling `heroku create your-app-name`

	- Heroku requires every app it hosts to have a totally unique name

8. Updates to your app are sent through Git, but this requires Git to know which remote repository to push to. To set the remote repository, call `heroku git:remote -a your-app-name`

9. The repository is now linked to a new Heroku app. To deploy changes to your app at any time, just use Git.

	1. `git add .` to queue modified files to be committed

	2. `git commit -m "Description of changes here" to save a snapshot of the codebase

	3. `git push heroku master` to send that snapshot to Heroku

		- This will automatically cause Heroku to redeploy your app with the changes.

## Understanding the Boilerplate's Structure