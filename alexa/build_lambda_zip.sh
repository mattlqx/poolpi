#!/bin/sh

SCRIPT_PATH=$(dirname $(realpath $0))
OLD_PWD=$PWD
cd $SCRIPT_PATH
cp ../location.py .
pip install -r requirements.txt --target .
if [ -e ask-lambda.zip ]; then rm -f ask-lambda.zip; fi
zip -D -r ask-lambda.zip * -x *.pyc
cd $OLD_PWD
