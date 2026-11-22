Changelog
---------

1.0.0 (unreleased)
~~~~~~~~~~~~~~~~~~

- Add type hints.
  [Daverball]

- Switch to ``pyproject.toml`` based project setup.
  [Daverball]

- Switch to ``src-layout`` based file structure.
  [Henri Hulski]

- Switch to a PEP-420 namespace package.
  [Daverball]

- Add support for Python 3.11 - 3.15.
  [Daverball & Henri Hulski]

- Drop support for Python below 3.11.
  [Daverball & Henri Hulski]

- Support Pypy 3.12.
  [Henri Hulski]

- Switch from black, flake8, isort and pyupgrade to Ruff_ linter and formatter.
  [Henri Hulski]

  .. _Ruff: https://docs.astral.sh/ruff

- Replace ``pre-commit`` integration with our custom tracked
  pre-commit git hook for Ruff checks on staged Python files.
  [Henri Hulski]

- Fix linting errors.

- Update ``README.rst``.

- Remove coveralls integration.

- Use GitHub Actions for CI.

- Adjust the deployment strategy:
  
  * Move the Pypi upload from ``zest.release`` to ``gh-actions``.

  * Use ``v`` + version as release tags like ``v1.0.0``.

  * So we still use ``zest.release`` but without publishing to Pypi.
    The Pypi upload is triggered by pushing the new release tag to GitHub.
    This happens in the Release workflow in ``.github/workflows/release.yml``.
    With this workflow we get Trusted Publishing with short-lived OIDC tokens
    that PyPI issues to one specific repository, workflow file and environment (``pypi``).
    We also get PEP 740 provenance and can set required reviewers for the environment
    and a ruleset who can create release tags and trigger releases.

  [Henri Hulski]

- Make an overall cleanup.

0.0.2 (2016-04-18)
~~~~~~~~~~~~~~~~~~~

- Adds compatibility with Morepath 0.14+.
  [Henri Hulski]

0.0.1 (2015-04-29)
~~~~~~~~~~~~~~~~~~~

- Initial release
  [href]
