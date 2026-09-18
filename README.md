# TradeLab

AI Assisted Stock Research Platform

## Features

- FastAPI
- Docker
- Structured Logging

## Run

```bash
cp .env.example .env
```

```bash
docker compose up --build
```

Open 

```
http://localhost:8000/docs
```
or 
```
http://localhost:8000/health
```

Test (set pytest with current dir explicitly on PYTHONPATH)

```bash
$env:PYTHONPATH = "."
pytest -vs tests/test_health.py
```
or 
```bash
python -m pytest -vs tests/test_health.py
```

## TODO

- stock model
- stock api
- stockservice
- yfinance
- db persistence

## Testing

Standard Status Codes -> 

1xx -> WAIT/INFORMATIONAL

2xx -> SUCCESS
	200 - ok/exists (for successful GET)
	201 - resource created (for successful POST)
	202 - async accepted (for async processing)
	203 - non-authoritative information
	204 - no content (for successful DELETE)

3xx -> REDIRECT/CACHE
	301 - permanent
	302 - temporary
	304 - not modified
	307 - temporary + preserve method
	308 - permanent + preserve method

4XX -> CLIENT/REQUEST PROBLEM
	400 - bad request
	401 - unauthenticated (who are you?)
	403 - unauthorized (you're not allowed)
	404 - resource absent (doesn't exist)
	405 - wrong HTTP method
	409 - state conflict/duplicate/concurrency conflict
	412 - precondition failed
	413 - payload too large
	415 - wrong/unsupported content type
	422 - validation failed
	429 - rate limited (too many requests)

5XX -> SERVER/DEPENDENCY PROBLEM
	500 - server failure (i crashed)
	502 - bad upstream response
	503 - service unavailable/overloaded
	504 - upstream timed out

### API Testing Checklist

POST /
	200/201, 400, 401, 403, 409, 413, 415, 422, 429, 500, 503

GET /
	200, 401, 403, 404, 429, 500, 503

DELETE /
	204, 401, 403, 404, 409, 500

### Steps

initialise alembic once 
$> alembic init alembic
creates alembic folder


create migration
$> docker exec -it tradelab-api-1 alembic revision --autogenerate -m "create users table"
run alembic inside API container/docker image, where db resolves correctly
$> docker exec -it tradelab-api-1 alembic upgrade head
now users table exists
check migration status
$> docker exec -it tradelab-api-1 alembic current
$> docker exec -it tradelab-api-1 alembic history


basic flow is :
sqlalchemy models -> alembic revision --autogenerate -> alembic/versions/<migration>.py -> alembic upgrade head -> postgresql tables


Docker Commands
(main start) start image, creating missing containers if needed
$> docker compose up -d

(main stop) stop docker container without deleting db volume
$> docker compose stop

check status
$> docker compose ps

inspect errors
$> docker compose logs -f api

rebuild api only
$> docker compose build api

start existing image
$> docker compose start

after dockerfile/dependencies changes
$> docker compose up -d --build api

$> forces a fresh build (avoid for routine iterations)
docker compose build --no-cache api