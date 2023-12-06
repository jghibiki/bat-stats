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