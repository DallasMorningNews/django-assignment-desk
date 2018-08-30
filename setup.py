# Imports from python.  # NOQA
import os
from setuptools import find_packages
from setuptools import setup


# Imports from django-assignment-desk.
from assignment_desk import __version__


REPO_URL = 'https://github.com/DallasMorningNews/django-assignment-desk/'

PYPI_VERSION = '.'.join(str(v) for v in __version__)

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-assignment-desk',
    version=PYPI_VERSION,
    packages=find_packages(),
    # packages=find_packages(exclude=['demo']),
    include_package_data=True,
    license='AGPLv3',
    description='A simple app to manage newsroom staff assignments.',
    long_description=README,
    long_description_content_type='text/markdown',
    url=REPO_URL,
    download_url='{repo_url}archive/{version}.tar.gz'.format(**{
        'repo_url': REPO_URL,
        'version': PYPI_VERSION,
    }),
    author='Alma Washington and Allan James Vestal, The Dallas Morning News',
    author_email='newsapps@dallasnews.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.11.0',
        'django-bootstrap3~=9.0.0',
        'django-colorfield~=0.1.10',
        'django-editorial-staff~=0.7.4',
        # 'slacker~=0.9.0',
    ],
)
