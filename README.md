# Bat Stats API

*Generate Migrations:*

```
poetry run python manage.py makemigrations
```


*Run Migrations*:
```
 docker-compose exec web poetry run python manage.py migrate --noinput
```

Connect to db:
```
docker-compose exec db psql --username=django --dbname=bat_stats
````

*Create super user:*
```shell
docker-compose exec web poetry run python manage.py createsuperuser --username=joe --email=joe@example.com
```

*Re-generate tailwind css*
```shell
tailwindcss -i ./src/static/css/main.css -o ./src/static/css/output.css --minify
```


Notes:
- django hdmx
  - https://django-htmx.readthedocs.io/en/latest/index.html
- htmx documentation
  - https://htmx.org/docs/#boosting
- guide for using tailwind, django, htmx
  - https://testdriven.io/blog/django-htmx-tailwind/
- django_components
  - https://github.com/EmilStenstrom/django-components