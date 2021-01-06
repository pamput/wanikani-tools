import urllib.parse

import pkg_resources
from mako.template import Template
from flask import render_template_string

import app.utils.wanikani_utils as utils


def get_kanji_drills(token, level=1, size=50, seed=None, only=None):
    if token is None:
        raise Exception("No token found")

    kanji = _get_kanji(token)
    kanji = _parse_kanji_response(kanji)

    max_level = int(len(kanji) / size) + (1 if len(kanji) % size > 0 else 0)

    info = {
        'level': level,
        'levels': max_level,
        'next_level_url': 'drills?' + urllib.parse.urlencode({
            'token': token,
            'level': level + 1 if level + 1 <= max_level else max_level,
            'size': size
        }),
        'prev_level_url': 'drills?' + urllib.parse.urlencode({
            'token': token,
            'level': level - 1 if level - 1 > 0 else 1,
            'size': size
        }),
        'total': len(kanji),
        'size': size
    }

    start = size * (level - 1)
    stop = min(start + size, len(kanji))
    kanji = kanji[start:stop]

    if only is not None and only is not '':
        only = [k for k in only]
        kanji = [k for k in kanji if k['kanji'] in only]

    return render_template_string(
        Template(
            pkg_resources.resource_string(__name__, 'template.html').decode(encoding='utf-8')
        ).render(kanji=kanji, info=info)
    )


def _get_kanji(token):
    return utils.get_all_kanji(token)


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
        'Flat Objects Counter': 'Flat Objects',
        'Formal Name Title': '-Sama'
    }

    return m.get(r, r)
