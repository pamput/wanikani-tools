# wanikani-tools

Simple tools for wanikani (https://www.wanikani.com/).

You can run this as simple script or as a flask server.

Requires **python 3** with the following modules:

- request
- flask (if running as server)
- mako

## Run as Script

```bash
python main ACTION V2_TOKEN
```

`ACTION` can be:

- `verbs`: shows all verbs up to the user's level
- `fails`: shows all failed reviews for the past 7 days (ignores subjects of the current level)
- `burned`: shows all burned kanji
- `kanji-poster`: generates a kanji poster (all 60 levels)

## Run as Flask Server

Run locally:

```bash
flask run
```

Server will available at http://localhost:5000

Available endpoints:

- `http://localhost:5000/fails?token=<V2_TOKEN>`: shows all learned verbs
- `http://localhost:5000/verbs?token=<V2_TOKEN>`: shows all failed reviews for the past 7 days
- `http://localhost:5000/burns?token=<V2_TOKEN>`: shows all burned kanji
- `http://localhost:5000/poster?token=<V2_TOKEN>`: generates a kanji poster (all 60 levels)

### As a Docker container

You can run the flask server as a docker container by building the available docker file. The container will be serving port `5000`.