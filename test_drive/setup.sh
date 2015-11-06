#!/usr/bin/env bash
SCRIPT_DIR=`dirname $0`
mkdir -p "${TEST_DRIVE_DIR:=/tmp/gremlin-python-test-drive}"

curl -L "http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.0/jython-installer-2.7.0.jar" -o "$TEST_DRIVE_DIR/jython-installer.jar"
java -jar "$TEST_DRIVE_DIR/jython-installer.jar" -s -d "$TEST_DRIVE_DIR/jython-2.7.0"

curl -L "http://s3.thinkaurelius.com/downloads/titan/titan-0.5.4-hadoop2.zip" -o "$TEST_DRIVE_DIR/titan-0.5.4-hadoop2.zip"

unzip -o "$TEST_DRIVE_DIR/titan-0.5.4-hadoop2.zip" -d "$TEST_DRIVE_DIR"

export GREMTHON_JAR_DIRS="$TEST_DRIVE_DIR/titan-0.5.4-hadoop2/lib"

curl -L "https://github.com/pokitdok/gremlin-python/releases/download/0.2.1/gremlin-python-0.2.1.jar" -o "$GREMTHON_JAR_DIRS/gremlin-python-0.2.1.jar"
curl -L "http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar" -o "$GREMTHON_JAR_DIRS/jython-standalone-2.7.0.jar"

cp "$SCRIPT_DIR/rexster-test-drive.xml" "$TEST_DRIVE_DIR/titan-0.5.4-hadoop2/conf/rexster-cassandra-es.xml"
