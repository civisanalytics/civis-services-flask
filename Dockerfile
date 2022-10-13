FROM python:3.10-slim-buster
LABEL maintainer=tech@civisanalytics.com

ENV APP_CONFIG_FILE=/app/civis_app/config/production.py

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./entrypoint.sh .
CMD ./entrypoint.sh
