from flask import Flask
from flask import Response
from flask import request

import app.burned_kanji.burned_kanji as burned
import app.kanji_csv.kanji_csv as csv
import app.kanji_drills.kanji_drills as drills
import app.kanji_poster.kanji_poster as poster
import app.recent_fail.recent_fail as fails
import app.verbs_export.verbs_to_html as verbs

app = Flask(__name__)


@app.route("/fails")
def do_fails():
    return fails.get_recent_fails_html(
        request.args.get('token', type=str)
    )


@app.route("/verbs")
def do_verbs():
    return verbs.get_all_verbs(
        request.args.get('token', type=str)
    )


@app.route("/burns")
def do_burns():
    return burned.get_burned_kanji(
        request.args.get('token', type=str)
    )


@app.route("/poster")
def do_poster():
    return poster.get_kanji_poster(
        request.args.get('token', type=str)
    )


@app.route("/csv")
def do_csv():
    return Response(
        csv.get_kanji_csv(
            request.args.get('token', type=str)
        ),
        mimetype='text/csv'
    )


@app.route("/drills")
def do_drills():
    return drills.get_kanji_drills(
        request.args.get('token', type=str),
        level=request.args.get('level', type=int, default=1),
        size=request.args.get('size', type=int, default=50),
        only=request.args.get('only', type=str)
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
