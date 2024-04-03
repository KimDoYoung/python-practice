#! /bin/bash
echo "====================================================================="
echo " Running tests for Joanna"
echo "====================================================================="
export JOANNA_MODE=local
export PYTHONPATH=/c/Users/deHong/Documents/kdy/python-practice/joanna
export PYTHONPATH=$PYTHONPATH:/c/Users/deHong/Documents/kdy/python-practice/joanna/backend
echo "MODE: $JOANNA_MODE"
echo "PYTHONPATH: $PYTHONPATH"
pytest backend/tests -v -s
