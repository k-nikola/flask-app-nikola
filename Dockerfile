FROM python:3.10.1

COPY . /usr/local/flaskapp

WORKDIR /usr/local/flaskapp

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "sh", "./entrypoint.sh" ]
