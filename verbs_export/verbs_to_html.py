import pkg_resources
import requests

import utils.wanikani_utils as utils


def get_all_verbs(token):
    if token is None:
        raise Exception("No token found")

    level = utils.get_user_level(token)

    levels_str = ",".join(str(i) for i in range(1, level + 1))

    r = requests.get(
        'https://api.wanikani.com/v2/subjects?types=vocabulary&levels={}'.format(levels_str),
        headers=utils.get_header(token)
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
            headers=utils.get_header(token)
        ).json()

        verbs.extend(extract_verbs(r))

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
    for v in verbs:
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

    return template.replace("{verbs}", code).replace("{verbs_amount}", str(len(verbs)))
