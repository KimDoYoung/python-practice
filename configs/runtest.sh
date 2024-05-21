#! /bin/bash
echo "====================================================================="
echo " Running tests for Joanna"
echo "====================================================================="
export JOANNA_MODE=local
base=/c/Users/deHong/Documents/kdy/python-practice/joanna
backend=/c/Users/deHong/Documents/kdy/python-practice/joanna/backend
exception=/c/Users/deHong/Documents/kdy/python-practice/joanna/backend/app/core/exceptions
export PYTHONPATH=$base:$backend:$exception
echo "MODE: $JOANNA_MODE"
echo "PYTHONPATH: $PYTHONPATH"
pytest backend/tests -v -s
