import os
import pickle
import tempfile

import requests


def get_all_kanji(token):
    cache_file = _get_kanji_pickle(token)
    if os.path.exists(cache_file):
        return _get_pickled_kanji(token)
    else:
        kanji = _get_all_kanji(token)
        _pickle_kanji(token, kanji)
        return kanji


def _get_all_kanji(token):
    kanji_response = requests.get(
        'https://api.wanikani.com/v2/subjects?types=kanji',
        headers=get_header(token)
    ).json()

    kanji = []
    kanji.extend(kanji_response['data'])

    while kanji_response['pages']['next_url']:
        kanji_response = requests.get(
            kanji_response['pages']['next_url'],
            headers=get_header(token)
        ).json()

        kanji.extend(kanji_response['data'])

    return kanji


def _get_kanji_pickle(token):
    return os.path.join(tempfile.gettempdir(), token, 'kanji.wk')


def _get_pickled_kanji(token):
    cache_file = _get_kanji_pickle(token)
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as kp:
            return pickle.load(kp)
    else:
        return None


def _pickle_kanji(token, kanji):
    cache_file = _get_kanji_pickle(token)

    if not os.path.exists(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))

    with open(cache_file, 'wb+') as kp:
        pickle.dump(kanji, kp)

    return cache_file


def get_user_level(token):
    return requests.get(
        'https://api.wanikani.com/v2/user',
        headers=get_header(token)
    ).json()['data']['level']


def get_header(token):
    return {
        'Authorization': 'Bearer ' + token
    }
