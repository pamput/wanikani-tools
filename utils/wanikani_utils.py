import requests


def get_user_level(token):
    return requests.get(
        'https://api.wanikani.com/v2/user',
        headers=get_header(token)
    ).json()['data']['level']


def get_header(token):
    return {
        'Authorization': 'Bearer ' + token
    }
