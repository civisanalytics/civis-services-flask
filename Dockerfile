FROM python:3.12-slim
LABEL maintainer=tech@civisanalytics.com

ENV APP_CONFIG_FILE=config/production.py
ENV PIP_ROOT_USER_ACTION=ignore

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./entrypoint.sh .
CMD ./entrypoint.sh
