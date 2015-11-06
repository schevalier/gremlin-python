#!/usr/bin/env bash
"${TEST_DRIVE_DIR:=/tmp/gremlin-python-test-drive}/titan-0.5.4-hadoop2/bin/titan.sh" start
"$TEST_DRIVE_DIR/titan-0.5.4-hadoop2/bin/rexster-console.sh" -l python
