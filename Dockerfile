FROM python:3.9.0-alpine

WORKDIR /usr/src/app

RUN pip install requests flask mako

COPY . .

CMD ["python", "app.py" ]