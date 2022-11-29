FROM python:3.9.15-slim-bullseye as app-image

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY config.yml /app/config.yml
COPY src /app/src
COPY docker/entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.txt

CMD /entrypoint.sh -c /app/config.yml
