#!/usr/bin/env bash
SCRIPT_DIR=`dirname $0`
export TEST_DRIVE_DIR="${TEST_DRIVE_DIR:=/tmp/gremlin-python-test-drive}"
"$TEST_DRIVE_DIR/titan-0.5.3-hadoop2/bin/titan.sh" start
"$TEST_DRIVE_DIR/titan-0.5.3-hadoop2/bin/rexster-console.sh" -l python -e "$SCRIPT_DIR/load_example_graph.py"
"$TEST_DRIVE_DIR/titan-0.5.3-hadoop2/bin/rexster-console.sh" -l python
