import os

from celery import Celery

app = Celery("celery")


app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")


@app.task()
def some_task(a: int, b: int):
    print(a, b)
    return "data"
