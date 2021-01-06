import os
import sys

from app import recent_fail as fails, kanji_drills as drills, burned_kanji as burned, verbs_export as verbs
from app.kanji_poster import kanji_poster as poster
from app.kanji_csv import kanji_csv as csv

if len(sys.argv) is not 3:
    raise Exception("USAGE: python main.py {verbs|fails} V2_TOKEN")

action = sys.argv[1]
token = sys.argv[2]
output = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.html')

with open(output, 'w+', encoding="utf-8") as html_file:
    actions = {
        'verbs': verbs.get_all_verbs,
        'fails': fails.get_recent_fails_html,
        'burned': burned.get_burned_kanji,
        'kanji-poster': poster.get_kanji_poster,
        'kanji-csv': csv.get_kanji_csv,
        'kanji-drills': drills.get_kanji_drills
    }

    html_file.write(actions[action](token))

print("Done: " + output)
