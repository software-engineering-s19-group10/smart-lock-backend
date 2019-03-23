# smart-lock-backend
Back-end database and REST API for the Smart Lock application.

## Installation
+ Clone the repo with `git clone`
+ Install `Python 3` and `pip` on your machine. `pip` is a package manager for Python.
+ Run `pip install virtualenv` to install `virtualenv`. This allows Python versions and libraries to be localized to the current project only.
+ Run `cd smart-lock-backend` to change into the project directory.
+ Run `virtualenv ./venv` to create a new Python virtual environment in the current directory.
+ Run `source venv/bin/activate` to start the virtual environment.
+ Run `pip install -r requirements.txt` to install all required libraries to run the project.


## Django and Django-Rest-Framework
+ Django and Django-Rest-Framework (DRF) are being used to create the database models. Using this, we can map URLs to specific database requests, and we can send data to and from the database through HTTP requests to the URLs.
+ For info about Django, see [the Django website](https://www.djangoproject.com/). Not all features of Django need to be used. In particular, no templating or advanced views need to be used.
+ For info about DRF, see [the website](https://www.django-rest-framework.org/). 
+ The basic implementation is as follows:
  + Create a database "model" - equivalent to just a table in a SQL database. Models are regular Python classes and can be manipulated as such, but most of the time you'll just need to use the built in Django model functions.
  + Define "serializers" - classes that essentially turn a model into JSON data, which we can send over HTTP in our API.
  + Define "views" - these are the endpoints of the API, where we define what happens when we get a certain request (i.e. GET, POST, PATCH, DELETE).
  + Associate URLs with the views - accessing these URLs invokes the view function.


## Running the Server Locally
+ From the project directory, use `python3 manage.py runserver` to run the testing environment.
+ From here, you can access the IP `127.0.0.1:8000` to view API endpoints (make sure you're appending the URL you want to the end).


## Changing the Database
+ When you change model classes, those changes need to be reconciled with the database that Django is interfacing with. This is done through migrations.
+ Run `python3 manage.py makemigrations` and then `python3 manage.py migrate` to reconcile changes LOCALLY ONLY.
+ To reconcile changes in production (on Heroku), you have to add `heroku run` to the beginning of the two commands above.


## Local vs Production
+ The local database is an SQLite database. The production database on Heroku is a PostgreSQL database. They behave pretty much the same for all of our uses, and SQLite is easier to work with locally.
+ When you make changes locally, they do not sync up to the production server immediately. You have to go through Heroku to deploy an update to production.


## Deploying to Production
+ First, install `heroku` on your machine.
+ Then, make an account on [heroku.com](https://www.heroku.com).
+ Run `heroku login` on your machine.
+ Run `heroku buildpacks:set heroku/python` to set deployment settings for a Python project.
+ Ask me (Mo) for access to the production repo. Heroku uses Git to manage deployment, so I'll have to add you as a collaborator.
+ Run `git add` and `git commit` with whatever you need.
+ Instead of pushing to origin, run `git push heroku master` to deploy to heroku.
+ If this doesn't work, see `DEPLOY.md` for a potential solution. I'll be logging any deployment problems I have along with their solutions in there for the time being.
