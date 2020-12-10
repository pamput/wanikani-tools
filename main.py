import os
import sys

import burned_kanji.burned_kanji as burned
import recent_fail.recent_fail as fails
import verbs_export.verbs_to_html as verbs
import kanji_poster.kanji_poster as poster
import kanji_csv.kanji_csv as csv
import kanji_drills.kanji_drills as drills

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
