import pkg_resources
import requests

import app.utils.wanikani_utils as utils


def get_burned_kanji(token):
    if token is None:
        raise Exception("No token found")

    level = utils.get_user_level(token)

    levels_str = ",".join(str(i) for i in range(1, level + 1))

    r = requests.get(
        'https://api.wanikani.com/v2/assignments?burned=true&subject_types=kanji&levels={}'.format(levels_str),
        headers=utils.get_header(token)
    ).json()

    def extract_kanji_ids(json):
        return map(lambda e: e['data']['subject_id'], json['data'])

    kanji_ids = []
    kanji_ids.extend(extract_kanji_ids(r))

    while r['pages']['next_url']:
        r = requests.get(
            r['pages']['next_url'],
            headers=utils.get_header(token)
        ).json()

        kanji_ids.extend(extract_kanji_ids(r))

    subject_request = requests.get(
        'https://api.wanikani.com/v2/subjects?ids={}'.format(','.join(map(str, kanji_ids))),
        headers=utils.get_header(token)
    ).json()

    def get_subjects(json):
        return json['data']

    kanji = get_subjects(subject_request)

    while subject_request['pages']['next_url']:
        subject_request = requests.get(
            subject_request['pages']['next_url'],
            headers=utils.get_header(token)
        ).json()

        kanji.extend(get_subjects(subject_request))

    raw_code = '''
            <tr>
                <td><span class="num"> {num} </span></td>
                <td><span class="kanji"> {slug} </span></td>
                <td><span class="reading"> {reading} </span></td>
                <td><span class="meaning"> {meaning} </span></td>
            </tr>
        '''

    code = ''
    num = 0
    for v in kanji:
        num += 1
        reading = ', '.join([str(x['reading']) for x in v['data']['readings']])
        meaning = ', '.join([str(x['meaning']) for x in v['data']['meanings']])

        data = {
            'num': num,
            'slug': v['data']['slug'],
            'reading': reading,
            'meaning': meaning,
        }

        code += raw_code.format(**data)

    template = pkg_resources.resource_string(__name__, 'template.html').decode(encoding='utf-8')

    return template.replace("{kanji}", code).replace("{kanji_amount}", str(len(kanji)))
