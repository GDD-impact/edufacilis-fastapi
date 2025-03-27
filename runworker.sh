celery -A app.workers.celery_app.c_app worker --loglevel=INFO &

celery -A app.workers.celery_app.c_app flower