import pkg_resources
import requests
from mako.template import Template

import utils.wanikani_utils as utils


def get_kanji_poster(token):
    if token is None:
        raise Exception("No token found")

    kanji = _get_kanji(token)
    kanji = _parse_kanji_response(kanji)

    return Template(
        pkg_resources.resource_string(__name__, 'template.html').decode(encoding='utf-8')
    ).render(kanji=kanji)


def _get_kanji(token):
    kanji_response = requests.get(
        'https://api.wanikani.com/v2/subjects?types=kanji',
        headers=utils.get_header(token)
    ).json()

    kanji = []
    kanji.extend(kanji_response['data'])

    while kanji_response['pages']['next_url']:
        kanji_response = requests.get(
            kanji_response['pages']['next_url'],
            headers=utils.get_header(token)
        ).json()

        kanji.extend(kanji_response['data'])

    return kanji


def _parse_kanji_response(kanji):
    response = []
    for k in kanji:
        response.append({
            'kanji': k['data']['characters'],
            'meaning': next(_fix_meaning(m['meaning']) for m in k['data']['meanings'] if m['primary']),
            'reading': next(r['reading'] for r in k['data']['readings'] if r['primary'])
        })

    return response


def _fix_meaning(r):
    m = {
        'Number In A Series': 'Number',
        'Ordinal Number Prefix': 'Ordinal Number',
        'Government Office': 'Office',
        'Flat Objects Counter': 'Flat Objects'
    }

    return m.get(r, r)
