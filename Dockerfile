FROM python:latest

COPY . /flaskapp

WORKDIR /flaskapp

RUN pip3 install -r requirements.txt

CMD [ "run.py" ]