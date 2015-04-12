import morepath

from itsdangerous import TimestampSigner, SignatureExpired, BadSignature
from uuid import uuid4 as new_uuid


class IdentityPolicy(object):
    """ A Morepath IdentityPolicy that stores attributes of the identity
    as cookies with a signature.

    You probably want to override this class in your application, to fit it
    to your needs.

    Don't use if your userid is a secret nobody should ever know. This
    policy *signs* values, it doesn't encrypt or hide them.
    """

    def __init__(self, max_age=3600, secure=True, httponly=True):
        """ Configures the identity policy with the following values:

        :max_age:
            The max age of both the signature and the cookie in seconds.
            Defaults to 3600 seconds.

        :secure:
            True if the cookies should only be transmitted over https.
            Defaults to True.

        :httponly:
            True if the cookies should not be accessible through client side
            scripts. Defaults to True.

        """
        self.max_age = max_age
        self.secure = secure
        self.httponly = httponly

    @morepath.reify
    def secret(self):
        """ The secret used to for the signatures.

        As long as the secret is not stored anywhere, the signed values all
        become invalid every time the secret is changed. Currently, that
        would mean that logged in users would be logged out if the
        application is restarted.

        """
        return new_uuid().hex

    @property
    def identity_class(self):
        """ The identity class to use. """
        return morepath.security.Identity

    @property
    def required_keys(self):
        """ The attributes of the identity which are signed and stored as
        cookies.

        This is useful to add additional values that are present on your
        identity. See the additional keyword values in the default identity:

        http://morepath.readthedocs.org/en/latest/api.html
        #morepath.security.Identity

        Note that those values are send in *cleartext*! So do not add
        information that is absolutely secret.

        """

        return ('userid', )

    @property
    def cookie_settings(self):
        """ Returns the default cookie settings.

        See also:

        http://webob.readthedocs.org/en/latest/modules/webob.html
        #webob.response.Response.set_cookie

        """
        return {
            'max_age': self.max_age,
            'secure': self.secure,
            'httponly': self.httponly
        }

    def identify(self, request):
        """ Returns the identity of the given request, if *all* cookies
        match, or None.

        """
        signatures = {
            k: self.unsign(request.cookies.get(k), salt=k)
            for k in self.required_keys
        }

        if None in signatures.values():
            return None
        else:
            userid = signatures.pop(self.required_keys[0])

            return self.identity_class(userid, **signatures)

    def remember(self, response, request, identity):
        """ Stores the given identity in the cookies of the response. """
        for key in self.required_keys:
            signed_value = self.sign(getattr(identity, key), salt=key)
            response.set_cookie(key, signed_value, **self.cookie_settings)

    def forget(self, response, request):
        """ Removes the identity from the cookies, basically forgetting it. """
        for key in self.required_keys:
            response.delete_cookie(key)

    def sign(self, unsigned_value, salt):
        """ Signs a value with a salt using itsdangerous.TimestampSigner and
        returns the resulting signed value.

        The salt might not be what you think it is:
        http://pythonhosted.org/itsdangerous/#the-salt
        """
        return TimestampSigner(self.secret, salt=salt).sign(unsigned_value)

    def unsign(self, signed_value, salt):
        """ Takes the signed value and returns it unsigned, if possible.

        If the signature is bad or if it expired, None is returned.
        """

        if not signed_value:
            return None

        signer = TimestampSigner(self.secret, salt=salt)

        try:
            unsigned = signer.unsign(signed_value, max_age=self.max_age)

            # see http://pythonhosted.org/itsdangerous/#python-3-notes
            return unsigned.decode('utf-8')

        except (SignatureExpired, BadSignature):
            return None
