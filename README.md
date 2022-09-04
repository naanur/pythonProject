## Тестовое задание

Для авторизации используется service_account.json

Ссылка на таблицу с данными для чтения 
[ссылка](https://docs.google.com/spreadsheets/d/1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0/edit?usp=sharing)
0. Change TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to your own in docker-compose.yml > web > environment:
1. Run docker compose
```
docker compose up -d
```
2. Look for the container name and ID
```
docker ps
```
3. copy the service_account.json to the container
```
docker cp .\service_account.json <CONTAINER ID>:/service_account.json
```

4. run background worker to collect data from google sheet 
```
docker exec -it pythonproject-web-1 python worker.py
```
3. React Frontend at http://0.0.0.0:3000
4. Django Backend at http://0.0.0.0:8000/api


