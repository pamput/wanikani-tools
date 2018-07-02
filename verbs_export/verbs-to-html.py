import os
import sys

import markdown
import requests

token = sys.argv[1]

if token is None:
    print("No token found")
    exit(1)

desktop_output = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.html')

level = 20
headers = {
    'Authorization': 'Bearer ' + token
}

levels_str = ",".join(str(i) for i in range(1, level + 1))

r = requests.get(
    'https://api.wanikani.com/v2/subjects?types=vocabulary&levels={}'.format(levels_str),
    headers=headers
).json()


def extract_verbs(json):
    verb_list = []
    for e in json['data']:
        if 'godan_verb' in e['data']['parts_of_speech']:
            verb_list.append(e)
        if 'ichidan_verb' in e['data']['parts_of_speech']:
            verb_list.append(e)

    return verb_list


verbs = []
verbs.extend(extract_verbs(r))

while r['pages']['next_url']:
    r = requests.get(
        r['pages']['next_url'],
        headers=headers
    ).json()

    verbs.extend(extract_verbs(r))

markdown_code = '| **Kanji** | **Reading** | **Meaning** |\n'
markdown_code += '| ---- | ---- | ---- |\n'

for v in verbs:
    reading = ', '.join([str(x['reading']) for x in v['data']['readings']])
    meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings']])

    data = {
        'slug': v['data']['slug'],
        'reading': reading,
        'meaning': meaning,
    }

    markdown_code += '| {slug} | {reading} | {meaning} |\n'.format(**data)


with open(desktop_output, 'w+', encoding="utf-8") as html_file:
    template = open(os.path.join(sys.path[0], 'template.html'), 'r').read()
    markdown_table = markdown.markdown(markdown_code, extensions=['markdown.extensions.tables'])

    html_file.write(
        template.replace("{body}", markdown_table)
    )

print("Done: " + desktop_output)
