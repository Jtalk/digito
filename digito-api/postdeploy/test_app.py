import os
from unittest import TestCase

import requests
from waiting import wait

_API_URL_ENV_VAR = 'API_URL'

_API_URL = os.getenv(_API_URL_ENV_VAR)
_ORIGIN_HOST = _API_URL.split('//', 1)[1].split('/', 1)[0] if _API_URL is not None else None

_SCRIPT_LOCATION = os.path.dirname(os.path.abspath(__file__))

_FILE_LOCATION = '%s/resources/test-image.png' % _SCRIPT_LOCATION
_FILE_DIGIT_VALUE = 3


def _api(suffix):
    return '%s%s' % (_API_URL, suffix)


def _check_health():
    health_check_url = _api('/health')
    print('Health check before testing:', health_check_url)
    r = requests.get(health_check_url)
    assert r.status_code == 200, 'Unexpected healthcheck failure: %s %s\n%s' \
                                 % (r.status_code, r.reason, r.text)
    print('Health check OK')
    return True


def _wait_service_up():
    wait(lambda: _check_health(),
         waiting_for='Service to start up',
         timeout_seconds=15,
         sleep_seconds=1,
         expected_exceptions=requests.exceptions.ConnectionError,
         )


class IntegrationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        assert _API_URL is not None, 'Application URL host must be supplied with %s' % _API_URL_ENV_VAR

    def test_requests(self):
        _wait_service_up()
        for i in range(10):
            print('Running recognition', i)
            with open(_FILE_LOCATION, 'rb') as f:
                r = requests.post(_api('/recognise'),
                                  headers={'Host': _ORIGIN_HOST},
                                  files={'image': f})
                self.assertTrue(r.ok, 'Unexpected response: %s %s\n%s' % (r.status_code, r.reason, r.text))
                recognised_digit = r.text
                self.assertEqual(str(_FILE_DIGIT_VALUE), recognised_digit, 'Wrong digit')


