# voteX
### Celery and Redis Configuration
```bash
## if you have redis installed locally you can skip this 
docker run --name redis -p 6379:6379 redis
docker exec -it redis sh

# using local redis installation (ensure to add redis to env path)
redis-server
redis-cli

## to start celery worker (on windows)
celery -A config worker -l INFO --pool=solo

## to start celery worker (on other OS)
celery -A config worker -l INFO

## Add this to  `.env` 

# CELERY
CELERY_BROKER_URL=redis://127.0.0.1:6379

## OR

cp .env.sample .env
```