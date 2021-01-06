FROM python:3.9.0-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install .

CMD ["python", "wanikani-tools/app.py" ]