import morepath
import time

from more.itsdangerous import IdentityPolicy


class TestRequest(object):
    cookies = {}


class TestResponse(TestRequest):
    cookie_args = {}

    def set_cookie(self, key, value, **kwargs):
        self.cookies[key] = value
        self.cookie_args[key] = kwargs

    def delete_cookie(self, key):
        if key in self.cookies:
            del self.cookies[key]
            del self.cookie_args[key]


def test_signatures():
    ip = IdentityPolicy()

    assert ip.unsign(ip.sign('admin', 'username'), 'username') == 'admin'
    assert ip.unsign(ip.sign('admin ', 'username'), 'username') == 'admin '
    assert ip.unsign(ip.sign('admin', 'username'), 'role') is None


def test_expired_signature():

    ip = IdentityPolicy(max_age=0.1)
    signed = ip.sign('admin', 'username')

    assert ip.unsign(signed, 'username') == 'admin'
    time.sleep(1.0)
    assert ip.unsign(signed, 'username') is None


def test_policy():
    ip = IdentityPolicy()
    identity = morepath.security.Identity(userid='aaron', role='admin')
    request = TestRequest()
    response = TestResponse()

    ip.remember(response, request, identity)

    assert 'userid' in response.cookies
    assert 'role' not in response.cookies


def test_custom_policy():

    class CustomIdentityPolicy(IdentityPolicy):
        required_keys = ('userid', 'role')

    ip = CustomIdentityPolicy()
    identity = morepath.security.Identity(userid='aaron', role='admin')
    request = TestRequest()
    response = TestResponse()

    ip.remember(response, request, identity)

    assert response.cookies['userid'].startswith(b'aaron.')
    assert response.cookies['role'].startswith(b'admin.')
    assert response.cookie_args['userid'] == response.cookie_args['role'] == {
        'max_age': 3600,
        'secure': True,
        'httponly': True
    }

    request.cookies = response.cookies

    assert ip.identify(request).userid == 'aaron'
    assert ip.identify(request).role == 'admin'

    del request.cookies['role']

    assert ip.identify(request) is None

    ip.forget(response, request)

    assert response.cookies == {}


def test_cookie_settings():
    ip = IdentityPolicy()
    assert ip.cookie_settings['max_age'] == 3600
    assert ip.cookie_settings['secure']
    assert ip.cookie_settings['httponly']

    ip = IdentityPolicy(max_age=1, secure=False, httponly=False)
    assert ip.cookie_settings['max_age'] == 1
    assert not ip.cookie_settings['secure']
    assert not ip.cookie_settings['httponly']
