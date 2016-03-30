import mock
import requests


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

    def test_url_creation(self):
        m_req = mock.Mock()
        m_cpb = mock.Mock()

        get_project_bandwidth('foo', _requests=m_req, _cpb=m_cpb)

        m_req.get.assert_called_once_with('https://pypi.python.org/pypi/foo/json')

    def test_response_json_sent_to_calc_project_bandwidth(self):
        m_req = mock.Mock()
        m_resp = m_req.get.return_value
        m_resp_json = m_resp.json
        m_cpb = mock.Mock()

        get_project_bandwidth('foo', _requests=m_req, _cpb=m_cpb)

        m_resp_json.assert_called_once_with()

        m_cpb.assert_called_once_with(m_resp_json.return_value)
