# wanikani-tools

Simple tools for wanikani (https://www.wanikani.com/).

You can un this as simple script or as a flask server.

Requires *python 3* with the following modules:

- requets
- flask (if running as server)

## Run as Script

```bash
python main ACTION V2_TOKEN
```

`ACTION` can be:

- `verbs`: shows all learned verbs
- `failed`: shows all failed reviews for the past 7 days

## Run as Flask Server

Run locally:

```bash
flask run
```

Server will available at http://localhost:5000

Available endpoints:

- `http://localhost:5000/<V2_TOKEN>/fails`: shows all learned verbs
- `http://localhost:5000/<V2_TOKEN>/verbs`: shows all failed reviews for the past 7 days

### As a Docker container

You can run the flask server as a docker container by building the available docker file. The container will be serving port `5000`.