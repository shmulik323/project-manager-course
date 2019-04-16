# working-with-flask

> flask rest api

## Build Setup

```bash
# install dependencies
$ pip install pipenv
$ pip install -r requirements.txt

# build for production and launch server
$ pipenv shell
$ cd <project-name> #where the manage.py is located
$ python manage.py db init
$ python manage.py db migrate
$ python appserver.py

```

For detailed explanation on how things work, checkout [Flask docs](http://flask.pocoo.org/docs/1.0/).
