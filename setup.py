from setuptools import setup, find_packages

name = "more.itsdangerous"
description = "An identity policy for morepath using itsdangerous."
version = "0.0.2"


def get_long_description():
    readme = open("README.rst", encoding="utf-8").read()
    history = open("HISTORY.rst", encoding="utf-8").read()

    # cut the part before the description to avoid repetition on pypi
    readme = readme[readme.index(description) + len(description) :]

    return "\n".join((readme, history))


setup(
    name=name,
    version=version,
    description=description,
    long_description=get_long_description(),
    url="http://github.com/morepath/more.itsdangerous",
    author="Seantis GmbH",
    author_email="info@seantis.ch",
    license="BSD",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=name.split(".")[:-1],
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=["itsdangerous", "morepath"],
    extras_require=dict(
        test=["coverage", "pytest"],
    ),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
)
