import requests
import requests_mock


def calc_project_bandwidth(project_data):
    total_bytes = 0
    if 'urls' not in project_data:
        return 0
    for url in project_data['urls']:
        total_bytes += url['size'] * url['downloads']
    return total_bytes


def get_project_bandwidth(project_name, _requests=requests, _cpb=calc_project_bandwidth):
    url = 'https://pypi.python.org/pypi/{0}/json'.format(project_name)
    resp = _requests.get(url)
    return _cpb(resp.json())


class TestGetProjectBandwidth(object):

    def test_all_with_requests_mock(self):
        with requests_mock.mock() as m:
            m.get('https://pypi.python.org/pypi/foo/json',
                  json={'urls': [{'downloads': 5, 'size': 10}]})

            assert get_project_bandwidth('foo') == 50
