# Dockerfile of Flask app
FROM python:3.7.4-alpine3.10

COPY ./app /app

WORKDIR /app

RUN apk --no-cache add postgresql-dev gcc python3-dev musl-dev && \
    pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

CMD ["/usr/local/bin/python3", "run.py"]
EXPOSE 5000