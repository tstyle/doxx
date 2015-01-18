#!/bin/sh

NOSE_FLAGS="--verbosity=2"
TEST_COMMAND="nosetests"

# Testing scripts

DOXX_KEYS="test_doxx-keys.py"
DOXX_TEMPLATES="test_doxx-templates.py"

# CLI

if [ "$1" = "all" ];then
    "$TEST_COMMAND" "$NOSE_FLAGS" "$DOXX_TEMPLATES" "$DOXX_KEYS"
elif [ "$1" = "keys" ];then
    "$TEST_COMMAND" "$NOSE_FLAGS" "$DOXX_KEYS"
elif [ "$1" = "templates" ]; then
    "$TEST_COMMAND" "$NOSE_FLAGS" "$DOXX_TEMPLATES"
else
    echo "Enter 'all' or a command suite to test."
    exit 1
fi