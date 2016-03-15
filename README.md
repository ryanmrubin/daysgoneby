# daysgoneby

Minimal, Heroku-deployable Django app to calculate days out of the country for immigration law purposes.

For dev setup (Ubuntu):

 1. Clone repo.
 2. From repo root: `python3.5 -m venv env`
 3. `source env/bin/activate`
 4. `pip install -r dev-requirements.txt`
 5. `export DJANGO_SETTINGS_MODULE='daysgoneby.settings.dev'`
 6. `./manage.py test`
 7. Verify tests pass.
 8. `./manage.py runserver`
 9. Verify server is running.

Here's a handy pair of aliases for you to tweak and use:

```
alias daysgoneby="cd /absolute/path/to/daysgoneby; source env/bin/activate; export DJANGO_SETTINGS_MODULE='daysgoneby.settings.dev'"
alias notdaysgoneby="deactivate; unset DJANGO_SETTINGS_MODULE; cd"

```
