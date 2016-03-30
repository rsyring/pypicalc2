import requests


def get_project_bandwidth(project_name):
    url = 'https://pypi.python.org/pypi/{0}/json'.format(project_name)
    resp = requests.get(url)
    return calc_project_bandwidth(resp.json())


def calc_project_bandwidth(project_data):
    total_bytes = 0
    if 'urls' not in project_data:
        return 0
    for url in project_data['urls']:
        total_bytes += url['size'] * url['downloads']
    return total_bytes


class TestCalcProjectBandwidth(object):

    def test_ok(self):
        data = {'urls': [{'downloads': 5, 'size': 10}]}
        assert calc_project_bandwidth(data) == 50

    def test_no_urls(self):
        data = {'urls': []}
        assert calc_project_bandwidth(data) == 0

    def test_no_url_key(self):
        data = {}
        assert calc_project_bandwidth(data) == 0
