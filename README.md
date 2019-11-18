# daysgoneby

[![Build Status](https://travis-ci.org/ryanmrubin/daysgoneby.svg?branch=master)](https://travis-ci.org/ryanmrubin/daysgoneby)

Minimal, Heroku-deployable Django app to calculate days out of the country for immigration law purposes.

For dev setup (Ubuntu):

 1. Clone repo.
 1. From repo root: `python3.5 -m venv env`
 1. `source env/bin/activate`
 1. `pip install -r dev-requirements.txt`
 1. `export DJANGO_SETTINGS_MODULE='daysgoneby.settings.dev'`
 1. `./manage.py test`
 1. Verify tests pass.
 1. `./manage.py runserver`
 1. Verify server is running.

Here's a handy pair of aliases for you to tweak and use:

```
alias daysgoneby="cd /absolute/path/to/daysgoneby; source env/bin/activate; export DJANGO_SETTINGS_MODULE='daysgoneby.settings.dev'"
alias notdaysgoneby="deactivate; unset DJANGO_SETTINGS_MODULE; cd"

```
