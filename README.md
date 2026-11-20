# CodeAlpha_SocialMedia — CodeAlpha Social Media Platform (Task 2)
Features: profiles, posts, comments, likes, follow

## Run
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000, register a user and start using it.
Tests: `python manage.py test`

Stack: Django, SQLite (can switch to MySQL in settings.py), Bootstrap 5.
