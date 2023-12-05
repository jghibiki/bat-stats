# Bat Stats API



*Run Migrations*:
```
 docker-compose exec web poetry run python manage.py migrate --noinput
```

Connect to db:
```
docker-compose exec db psql --username=django --dbname=bat_stats
````