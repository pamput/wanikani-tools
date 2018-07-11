FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install requests flask

COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]