from flask import Flask

import recent_fail.recent_fail as fails
import verbs_export.verbs_to_html as verbs

app = Flask(__name__)


@app.route("/<token>/fails")
def do_fails(token):
    return fails.get_recent_fails_html(
        token
    )


@app.route("/<token>/verbs")
def do_verbs(token):
    return verbs.get_all_verbs(
        token
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')