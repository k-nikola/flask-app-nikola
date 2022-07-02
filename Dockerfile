FROM python:3.10.1-slim

COPY . /flaskapp

WORKDIR /flaskapp

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "gunicorn" ]

CMD ["-w", "4", "-b", "0.0.0.0:5000", "webapp:app", "2>&1", ">>", "log.txt", "&"]
