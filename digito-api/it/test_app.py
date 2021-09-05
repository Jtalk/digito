import os
import random
import re
import string
import subprocess
import requests

from os import system
from shutil import which
from unittest import TestCase
from waiting import wait

_DOCKER_IMAGE_ENVVAR = 'IT_DOCKER_IMAGE_NAME'
_DOCKER_EXEC_ENVVAR = 'DOCKER_EXEC'

_ORIGIN_LOCATION_HOST = 'http://localhost'

_SCRIPT_LOCATION = os.path.dirname(os.path.abspath(__file__))
_IMAGE_NAME = os.getenv(_DOCKER_IMAGE_ENVVAR)
_DOCKER_EXEC = os.getenv(_DOCKER_EXEC_ENVVAR, "docker")

_FILE_LOCATION = '%s/resources/test-image.png' % _SCRIPT_LOCATION
_FILE_DIGIT_VALUE = 3


def _localhost(path):
    return 'http://localhost:%s%s' % (IntegrationTest.appPort, path)


def _check_health():
    health_check_url = _localhost('/health')
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

    appPort = None
    dockerContainerName = None

    @classmethod
    def setUpClass(cls):
        assert _IMAGE_NAME is not None, 'A name for the docker image to test must be provided as a %s' % _DOCKER_IMAGE_ENVVAR
        assert which(
            _DOCKER_EXEC) is not None, 'A docker executable must either be available in PATH, or provided as %s' % _DOCKER_EXEC_ENVVAR
        cls.dockerContainerName = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(20))
        cmd = '%s run --rm -d --name %s -e UI_LOCATION=%s -p ::80 %s' \
              % (_DOCKER_EXEC, cls.dockerContainerName, _ORIGIN_LOCATION_HOST, _IMAGE_NAME)
        print('Starting up the app: %s' % cmd)
        system(cmd)
        cls.appPort = IntegrationTest._get_docker_port(cls.dockerContainerName)
        print('The app is now running on localhost:%s' % cls.appPort)
        system('%s ps' % _DOCKER_EXEC)
        system('%s port %s' % (_DOCKER_EXEC, cls.dockerContainerName))

    @classmethod
    def tearDownClass(cls):
        cmd = '%s logs %s' % (_DOCKER_EXEC, cls.dockerContainerName)
        print('Printing container logs:', cmd)
        system(cmd)
        cmd = '%s stop %s' % (_DOCKER_EXEC, cls.dockerContainerName)
        print('Stopping the app:', cmd)
        system(cmd)

    @staticmethod
    def _get_docker_port(docker_container_name):
        out = subprocess.Popen([_DOCKER_EXEC, 'port', docker_container_name],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = out.communicate()
        regex = re.compile(
            '80/tcp\s+->\s+[\w\d.]+:(\d+)', re.M | re.IGNORECASE)
        match = regex.match(out.decode('UTF-8'))
        assert match is not None, 'Could not determine the host docker port: \n%s\n%s' % (
            repr(out), repr(err))
        return match.group(1)

    def test_requests(self):
        _wait_service_up()
        for i in range(10):
            print('Running recognition', i)
            with open(_FILE_LOCATION, 'rb') as f:
                r = requests.post(_localhost('/recognise'),
                                  headers={'Host': _ORIGIN_LOCATION_HOST},
                                  files={'image': f.read()})
                self.assertTrue(r.ok, 'Unexpected response: %s %s\n%s' % (
                    r.status_code, r.reason, r.text))
                recognised_digit = r.text
                self.assertEqual(str(_FILE_DIGIT_VALUE),
                                 recognised_digit, 'Wrong digit')
