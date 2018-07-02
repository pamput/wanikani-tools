import os
import sys
from datetime import datetime, timedelta

import markdown
import requests

token = sys.argv[1]
desktop_output = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.html')

if token is None:
    print("No token found")
    exit(1)

headers = {
    'Authorization': 'Bearer ' + token
}

past_str = (datetime.now() - timedelta(days=7)).isoformat()

review_request = requests.get(
    'https://api.wanikani.com/v2/reviews?updated_after={}'.format(past_str),
    headers=headers
).json()


def get_failed_reviews(json):
    failed = []
    for e in json['data']:
        if e['data']['incorrect_meaning_answers'] or e['data']['incorrect_reading_answers'] is not 0:
            failed.append(e)

    return failed


failed_reviews = []
failed_reviews.extend(get_failed_reviews(review_request))

while review_request['pages']['next_url']:
    review_request = requests.get(
        review_request['pages']['next_url'],
        headers=headers
    ).json()

    failed_reviews.extend(get_failed_reviews(review_request))

failed_reviews_ids = set()
failed_reviews_ids.update(map(lambda r: r['data']['subject_id'], failed_reviews))

subject_request = requests.get(
    'https://api.wanikani.com/v2/subjects?ids={}'.format(','.join(map(str, failed_reviews_ids))),
    headers=headers
).json()


def get_failed_subjects(json):
    vj = []
    kj = []
    for e in json['data']:
        if e['object'] == 'vocabulary':
            vj.append(e)
        if e['object'] == 'kanji':
            kj.append(e)

    return kj, vj


response = get_failed_subjects(subject_request)

kanji = []
kanji.extend(response[0])

vocabulary = []
vocabulary.extend(response[1])

while subject_request['pages']['next_url']:
    subject_request = requests.get(
        subject_request['pages']['next_url'],
        headers=headers
    ).json()

    response = (get_failed_subjects(subject_request))
    kanji.extend(response[0])
    vocabulary.extend(response[1])


kanji_markdown_code = '| **Kanji** | **Reading** | **Meaning** |\n'
kanji_markdown_code += '| ---- | ---- | ---- |\n'

for v in kanji:
    reading = ', '.join([str(x['reading']) for x in v['data']['readings']])
    meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings']])

    data = {
        'slug': v['data']['slug'],
        'reading': reading,
        'meaning': meaning,
    }

    kanji_markdown_code += '| {slug} | {reading} | {meaning} |\n'.format(**data)


vocabulary_markdown_code = '| **Kanji** | **Reading** | **Meaning** |\n'
vocabulary_markdown_code += '| ---- | ---- | ---- |\n'

for v in vocabulary:
    reading = ', '.join([str(x['reading']) for x in v['data']['readings']])
    meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings']])

    data = {
        'slug': v['data']['slug'],
        'reading': reading,
        'meaning': meaning,
    }

    vocabulary_markdown_code += '| {slug} | {reading} | {meaning} |\n'.format(**data)


with open(desktop_output, 'w+', encoding="utf-8") as html_file:
    template = open(os.path.join(sys.path[0], 'template.html'), 'r').read()
    kanji_markdown_table = markdown.markdown(kanji_markdown_code, extensions=['markdown.extensions.tables'])
    vocabulary_markdown_table = markdown.markdown(vocabulary_markdown_code, extensions=['markdown.extensions.tables'])

    html_file.write(
        template.replace("{kanji}", kanji_markdown_table).replace("{vocabulary}", vocabulary_markdown_table)
    )

print("Done: " + desktop_output)
