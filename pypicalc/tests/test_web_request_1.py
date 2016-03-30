import json

import requests


def get_project_bandwidth(project_name):
    url = 'https://pypi.python.org/pypi/{0}/json' \
        .format(project_name)
    resp = requests.get(url)

    data = json.loads(resp.text)
    total_bytes = 0
    for url in data['urls']:
        total_bytes += url['size'] * url['downloads']
    return total_bytes
