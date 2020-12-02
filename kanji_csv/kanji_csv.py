import pkg_resources
import requests
import csv
import io

import utils.wanikani_utils as utils


def get_kanji_csv(token):
    if token is None:
        raise Exception("No token found")

    kanji = _get_kanji(token)
    kanji = _parse_kanji_response(kanji)
    output = _get_csv(kanji)

    return output


def _get_csv(kanji):
    output = io.StringIO()
    writer = csv.writer(output)

    for k in kanji:
        row = [
            k['id'], k['kanji'], k['meaning'], k['reading']
        ]
        writer.writerow(row)

    return output.getvalue()


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
            'id': k['id'],
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
