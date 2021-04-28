FROM python:3.8-slim-buster


WORKDIR /home/usr

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install wheel
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install gunicorn

COPY website website
COPY run.py website/.env ./

ENV FLASK_APP run.py


CMD [ "python3", "-m","flask","run", "--host=0.0.0.0"]
