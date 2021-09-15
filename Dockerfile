FROM python:latest

COPY . /flaskapp

WORKDIR /flaskapp

RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn

CMD ["nohup", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "webapp:app", ">", "log.txt", "2>&1", "&"]