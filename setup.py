import io

from setuptools import find_packages
from setuptools import setup

import fuzza


with io.open('README.rst', 'rt') as f:
    README = f.read()

REQUIRES = [
    'click>=6.0',
    'ruamel.yaml>=0.15.0'
]

setup(
    name=fuzza.__prog__,
    version=fuzza.__version__,
    description=fuzza.__description__,
    long_description=README,
    author='C.X. Ling',
    author_email='rcxng93@hotmail.com',
    url='https://github.com/Raphx/fuzza.git',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    package_data={
        'fuzza.logger': ['logger.cfg.yml']
    },
    install_requires=REQUIRES,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'fuzza = fuzza.cli:cli'
        ]
    },
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Traffic Generation'
    )
)
