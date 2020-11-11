More Itsdangerous
=================

An identity policy for morepath using itsdangerous.

Usage
-----

.. code-block:: python

    import morepath
    from more.itsdangerous import IdentityPolicy

    class App(morepath.App):
        pass

    @App.identity_policy()
    def get_identity_policy():
        return IdentityPolicy()

    @App.verify_identity()
    def verify_identity(identity):
        # trust the identity established by the identity policy (we could keep
        # checking if the user is really in the database here - or if it was
        # removed in the meantime)
        return True

See `<http://morepath.readthedocs.org/en/latest/security.html>`_ to learn more
about Morepath's security model and and have
a look at the commented source code:

`<https://github.com/morepath/more.itsdangerous/blob/master/more/itsdangerous/identity_policy.py>`_

The IdentityPolicy class is meant to be extended because everyone has differing
needs. It simply provides a way to store the identity as a signed cookie, using
itsdangerous.

Usage in Development
--------------------

By default, the cookies created by more.itsdangerous are
`HttpOnly <http://en.wikipedia.org/wiki/HTTP_cookie#HttpOnly_cookie>`_ and
`Secure <http://en.wikipedia.org/wiki/HTTP_cookie#Secure_cookie>`_.

If you have differing needs or if you are running a development server you
might have to change the identity policy's configuration:

.. code-block:: python

    @App.identity_policy()
    def get_identity_policy():
        # make the cookies work under http, not just https
        return IdentityPolicy(secure=False)

Note that this should only be used in development. In this day and age you do
not want to transmit cookies over http!

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py38

Conventions
-----------

More Itsdangerous follows PEP8 as close as possible. To test for it run::

    tox -e pep8

More Itsdangerous uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.com/morepath/more.itsdangerous.png
  :target: https://travis-ci.com/morepath/more.itsdangerous
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/morepath/more.itsdangerous/badge.png?branch=master
  :target: https://coveralls.io/r/morepath/more.itsdangerous?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/more.itsdangerous.svg
  :target: https://crate.io/packages/more.itsdangerous
  :alt: Latest PyPI Release

License
-------
more.itsdangerous is released under the revised BSD license
