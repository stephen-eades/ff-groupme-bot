# Fantasy Football GroupMe Bot

Setup your league's own Fantasy Football data GroupMe chatbot to display important league data at your command. Could not have completed this without the work of @apnorton, @stmorse and @tpagliocco. 

This only works with public ESPN leagues currently.

## Setup

1. [Install Python 3](https://www.python.org/downloads/)

2. [Create a Heroku account](https://signup.heroku.com/)

3. [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

4. Clone this repository and navigate to the root with the Heroku CLI.

5. Add your ESPN league ID and plug in your GroupMe ID to the app.py variables. Adjust functions to fit your league. Note that historical data requests reach back as early as 2013, you can easily extend this in the code.

6. Log in to the Heroku CLI by calling `heroku login`

7. Initialize the Heroku app by calling `heroku create your-app-name`

8. To set the remote repository, call `heroku git:remote -a your-app-name`

9. The repository is now linked to a new Heroku app. To deploy a new version of your app at any time, just use Git.

	1. `git add .` to stage your changes

	2. `git commit -m "Description of changes here"` to commit your changes

	3. `git push heroku master` to push your commit to Git and build it on Heroku

	4. To view your app's logs while it is deployed, call `heroku logs -t`. This will show the logs in realtime.
