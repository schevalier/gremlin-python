#
# Copyright (C) 2015, All Rights Reserved, PokitDok, Inc.
# https://platform.pokitdok.com
#
# Please see the LICENSE file for more information.
# All other rights reserved.
#
"""
gremlin-python
--------------
gremlin-python (gremthon) allows you to use Python syntax when traversing property graphs.
Allows python scripts to be submitted for execution on rexster servers.

gremlin-python is distributed under the MIT License.
"""
from setuptools import setup


setup(
    name="gremlin-python",
    version="0.2.2",
    license="MIT",
    author="PokitDok, Inc.",
    author_email="platform@pokitdok.com",
    url="https://platform.pokitdok.com",
    download_url='https://github.com/pokitdok/gremlin-python/tarball/0.2.2',
    description="gremlin python allows you to use Python syntax when traversing property graphs",
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    py_modules=['gremthon'],
    test_suite='nose.collector',
    keywords=['tinkerpop', 'gremlin', 'titan', 'graph', 'rexster'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: Implementation :: Jython",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Java Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)