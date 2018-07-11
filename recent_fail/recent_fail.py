from datetime import datetime, timedelta

import pkg_resources
import requests

import utils.wanikani_utils as utils


def get_recent_fails_html(token):
    if token is None:
        raise Exception("No token found")

    level = utils.get_user_level(token)

    failed_reviews = _get_failed_reviews_after_date(
        token,
        datetime.now() - timedelta(days=7)
    )

    failed_reviews_ids = set()
    failed_reviews_ids.update(map(lambda r: r['data']['subject_id'], failed_reviews))

    kanji, vocabulary = _get_reviews_before_level(token, level, failed_reviews_ids)

    kanji_code = ''
    num = 0

    for v in kanji:
        num += 1
        reading = ', '.join([str(x['reading']) for x in v['data']['readings'] if str(x['reading']) != 'None'])
        meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings'] if str(x['meaning']) != 'None'])

        data = {
            'num': num,
            'slug': v['data']['slug'],
            'reading': reading,
            'meaning': meaning,
        }

        kanji_code += '''
            <tr>
                <td><span class="num"> {num} </span></td>
                <td><span class="kanji"> {slug} </span></td>
                <td><span class="reading"> {reading} </span></td>
                <td><span class="meaning"> {meaning} </span></td>
            </tr>
        '''.format(**data)

    vocabulary_code = ''
    num = 0

    for v in vocabulary:
        num += 1
        reading = ', '.join([str(x['reading']) for x in v['data']['readings'] if str(x['reading']) != 'None'])
        meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings'] if str(x['meaning']) != 'None'])

        data = {
            'num': num,
            'slug': v['data']['slug'],
            'reading': reading,
            'meaning': meaning,
        }

        vocabulary_code += '''
            <tr>
                <td><span class="num"> {num} </span></td>
                <td><span class="kanji"> {slug} </span></td>
                <td><span class="reading"> {reading} </span></td>
                <td><span class="meaning"> {meaning} </span></td>
            </tr>
        '''.format(**data)

    template = pkg_resources.resource_string(__name__, 'template.html').decode(encoding='utf-8')

    return template \
        .replace("{kanji}", kanji_code) \
        .replace("{vocabulary}", vocabulary_code) \
        .replace("{kanji_amount}", str(len(kanji))) \
        .replace("{vocabulary_amount}", str(len(vocabulary)))


def _get_reviews_before_level(token, level, reviews_ids):
    subject_request = requests.get(
        'https://api.wanikani.com/v2/subjects?ids={}'.format(','.join(map(str, reviews_ids))),
        headers=utils.get_header(token)
    ).json()

    def get_failed_subjects(json, level):
        vj = []
        kj = []
        for e in json['data']:
            if e['data']['level'] < level:
                if e['object'] == 'vocabulary':
                    vj.append(e)
                if e['object'] == 'kanji':
                    kj.append(e)

        return kj, vj

    response = get_failed_subjects(subject_request, level)

    kanji = []
    kanji.extend(response[0])

    vocabulary = []
    vocabulary.extend(response[1])

    while subject_request['pages']['next_url']:
        subject_request = requests.get(
            subject_request['pages']['next_url'],
            headers=utils.get_header(token)
        ).json()

        response = get_failed_subjects(subject_request, level)

        kanji.extend(response[0])
        vocabulary.extend(response[1])

    return kanji, vocabulary


def _get_failed_reviews_after_date(token, date):
    review_response = requests.get(
        'https://api.wanikani.com/v2/reviews?updated_after={}'.format(date.isoformat()),
        headers=utils.get_header(token)
    ).json()

    def get_failed_reviews(response):
        failed = []
        for e in response['data']:
            if e['data']['incorrect_meaning_answers'] or e['data']['incorrect_reading_answers'] is not 0:
                failed.append(e)

        return failed

    failed_reviews = []
    failed_reviews.extend(get_failed_reviews(review_response))
    while review_response['pages']['next_url']:
        review_response = requests.get(
            review_response['pages']['next_url'],
            headers=utils.get_header(token)
        ).json()

        failed_reviews.extend(get_failed_reviews(review_response))
    return failed_reviews
