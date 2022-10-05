FROM python:3.10.1

COPY . /flaskapp

WORKDIR /flaskapp

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "sh", "./entrypoint.sh" ]
