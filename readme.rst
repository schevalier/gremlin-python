.. image:: https://travis-ci.org/pokitdok/gremlin-python.svg?branch=master
    :target: https://travis-ci.org/pokitdok/gremlin-python


gremlin-python
==============

gremlin-python (gremthon) allows you to use Python syntax when traversing property graphs...

Quick Start
-----------

Take a test drive locally (expects curl, java, and unzip commands to be available):

.. code-block:: bash

    $ ./test_drive/setup.sh && ./test_drive/run.sh


This will download the necessary components, start titan, and run the rexster console with
python scripting support enabled.

If you prefer to use Docker, you can pull the pokitdok/gremlin-python-test-drive container and run it
to quickly evaluate gremlin-python:

.. code-block:: bash

    $ docker run -i -t pokitdok/gremlin-python-test-drive


Compile, test and package the gremlin-python jar:

.. code-block:: bash

    $ mvn clean package

rexster
-------

To utilize Python syntax from within a rexster console, you'll need to drop in a couple of jar files
and edit some xml configuration.

Edit conf/rexster-cassandra-es.xml (or the configuration file you're using) in your titan distribution directory to include:

.. code-block:: xml

        <script-engine>
            <name>gremlin-python</name>
        </script-engine>


See the rexster-test-drive.xml file for an example configuration that's used when you take a test drive.

You'll also need to put the files gremlin-python-{version}.jar and jython-standalone-{version}.jar
into your titan lib directory.   gremlin-python has been tested with jython-standalone-2.7.0.jar.
You can find a gremlin-python jar file for each release at https://github.com/pokitdok/gremlin-python/releases
The jython standalone jar can be found at http://www.jython.org/downloads.html

After (re)starting titan + rexster, you should see python available in your rexster console:


.. code-block:: bash

    $ ./bin/rexster-console.sh -l python
            (l_(l
    (_______( 0 0
    (        (-Y-) <woof>
    l l-----l l
    l l,,   l l,,
    opening session [127.0.0.1:8184]
    ?h for help

    rexster[python]> g = rexster.getGraph("graph")
    ==>null
    rexster[python]> from com.thinkaurelius.titan.example import GraphOfTheGodsFactory
    ==>null
    rexster[python]> GraphOfTheGodsFactory.load(g.graph)
    ==>null
    rexster[python]> [v.name for v in g.V]
    ==>nemean
    ==>jupiter
    ==>pluto
    ==>hydra
    ==>sky
    ==>tartarus
    ==>hercules
    ==>alcmene
    ==>cerberus
    ==>neptune
    ==>saturn
    ==>sea
    rexster[python]> [v.name for v in g.V if v.age]
    ==>jupiter
    ==>pluto
    ==>hercules
    ==>alcmene
    ==>neptune
    ==>saturn
    rexster[python]> [v.name for v in g.V.filter(lambda it: it.age > 4000)]
    ==>jupiter
    ==>neptune
    ==>saturn
    rexster[python]> g.V.has('name','hercules')
    ==>v[1536]
    rexster[python]> g.V.has('name','hercules').name
    ==>hercules
    rexster[python]> g.V.has('name','hercules').age
    ==>30


Troubleshooting
---------------

If you have problems connecting to a remote titan graph (that's using elasticsearch) when you're working
within an interactive jython session, try placing the names.txt file from elasticsearch somewhere on
the path or in your current working directory.  It seems that some class loader differences exist
between an interactive jython session and working within rexster.  names.txt can be found properly
within rexster but not when working with jython.  You can grab a copy of names.txt here:
https://github.com/elasticsearch/elasticsearch/blob/master/src/main/resources/config/names.txt
or from within the elasticsearch jar file.


Supported JVM Versions
----------------------

This library aims to support and is tested against these JVM versions:

* openjdk7
* oraclejdk7
* oraclejdk8


License
-------

Copyright (c) 2015 PokitDok, Inc.  The MIT License (MIT) (See LICENSE_ for details.)
