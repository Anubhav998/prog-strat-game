# prog-strat-gatme
A Turn Based, Progressional, Multiplayer, Online Strategy Game

![codeship](https://codeship.com/projects/ee51a930-dbb4-0132-4b09-428a02316898/status?branch=master)
[![Code Health](https://landscape.io/github/mc706/prog-strat-game/master/landscape.svg?style=flat)](https://landscape.io/github/mc706/prog-strat-game/master)
[![Coverage Status](https://coveralls.io/repos/mc706/prog-strat-game/badge.svg?branch=HEAD)](https://coveralls.io/r/mc706/prog-strat-game?branch=HEAD)

## Development Setup

There are a few requirements of this project for development

* python 2.7
* pip
* npm

There are a few steps for setting up the repository to start development:

1. Install Python Package Requirements

```
pip install -r requirements.txt
```

2. Install NodeJS Package Requirements

```
npm install
```

3. Install BowerJS Components

```
bower install
```

4. Create `local_settings.py`

Create a `progstrat/local_settings.py` to configure your local repo and what databse it should use


5. Sync and Migrate database

```
./manage.py syncdb
./manage.py migrate
```

## Making Changes

This repository follows 100% code coverage and holds itself to pep8 and jshint coding standards. To test the changes, 
first run.

```
fab test
```

This will check that coverage and code quaility are up to par. If all tests pass, commit your changes. Once you have a 
set of commits that you are ready to deploy, run

```
fab cut
```

This will run the tests, increment the version number, update the change log, tag a release, and push it all to github.


## Documentation

Further documentation around the codebase and other information, see `/docs/`