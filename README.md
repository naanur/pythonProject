## Тестовое задание

Для авторизации используется service_account.json

Ссылка на таблицу с данными для чтения 
[ссылка](https://docs.google.com/spreadsheets/d/1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0/edit?usp=sharing)

1. Run docker compose
```
docker compose up
```
2. Look for the container name
```
docker ps
```

3. run background worker to collect data from google sheet 
```
docker exec -it pythonproject-web-1 python worker.py
```
3. React Frontend at http://0.0.0.0:3000
4. Django Backend at http://0.0.0.0:8000/api


