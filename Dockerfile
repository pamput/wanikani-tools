FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN pip install requests flask

COPY . .

CMD ["python", "app.py" ]