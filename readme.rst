.. image:: https://travis-ci.org/pokitdok/gremlin-python.svg?branch=master
    :target: https://travis-ci.org/pokitdok/gremlin-python


gremlin-python
==============

gremlin-python (gremthon) allows you to use Python syntax when traversing property graphs...

local use
---------

Install jython in your home directory

Download http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7-b3/jython-installer-2.7-b3.jar

Run:

.. code-block:: bash

    $ java -jar jython-installer-2.7-b3.jar

jython doesn't seem to work well with pip so we'll use easy_install to fetch 3rd party dependencies:

.. code-block:: bash

    $ ~/jython2.7b3/bin/jython -c "$(curl -fsSL http://peak.telecommunity.com/dist/ez_setup.py)"

Then you can install additional dependencies like:

.. code-block:: bash

    $ ~/jython2.7b3/bin/easy_install nose
    $ ~/jython2.7b3/bin/easy_install rednose
    $ ~/jython2.7b3/bin/easy_install requests

You can load up an interactive jython session with all of the jars that ship with titan by setting
the GREMTHON_JAR_DIRS environment variable:

.. code-block:: bash

    $ export GREMTHON_JAR_DIRS=/Users/corbinbs/Downloads/titan-0.5.3-hadoop2/lib/

Run a local, interactive gremthon session:

.. code-block:: bash

    $ ~/jython2.7b3/bin/jython -i gremthon.py

That will automatically load up a sample graph so that you can follow http://gremlindocs.com/
except with Python syntax

Run all the python tests

.. code-block:: bash

    $ ~/jython2.7b3/bin/nosetests --rednose

Compile, test and package the gremlin-python jar:

.. code-block:: bash

    $ mvn clean package

rexter
------

To utilize Python syntax from within a rexster console, you'll need to drop in a couple of jar files
and edit some xml configuration.

Edit conf/rexster-cassandra-es.xml (or the configuration file you're using) in your titan distribution directory to include:

.. code-block:: xml

        <script-engine>
            <name>gremlin-python</name>
        </script-engine>


There should already be a script-engine defined for gremlin-groovy.   You can just paste that snippet for gremlin-python
below it.

You'll also need to drop the files gremlin-python-{version}.jar and jython-standalone-{version}.jar
into your titan lib directory.   gremlin-python has been tested with jython-standalone-2.7-b3.jar.

After restarting titan + rexster, you should see python available in your rexster console:


.. code-block:: bash

    ~/titan-0.5.3-hadoop2 $ ./bin/rexster-console.sh
            (l_(l
    (_______( 0 0
    (        (-Y-) <woof>
    l l-----l l
    l l,,   l l,,
    opening session [127.0.0.1:8184]
    ?h for help

    rexster[groovy]> ?python
    rexster[python]> from com.tinkerpop.blueprints.impls.tg import TinkerGraphFactory
    ==>null
    rexster[python]> from gremthon import Gremthon
    ==>null
    rexster[python]> graph = TinkerGraphFactory.createTinkerGraph()
    ==>null
    rexster[python]> g = Gremthon(graph)
    ==>null
    rexster[python]> list(g.v(3))[0].name
    ==>lop
    rexster[python]> [v.id for v in g.v(4).in_()]
    ==>1
    rexster[python]> g.v(1).out('knows').has('name','josh')
    ==>v[4]
    rexster[python]> g = Gremthon(rexster.getGraph("graph"))
    ==>null
    rexster[python]> g.V
