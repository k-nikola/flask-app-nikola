FROM python:latest


RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY . /flaskapp

WORKDIR /flaskapp

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]