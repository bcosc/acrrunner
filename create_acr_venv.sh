#!/bin/bash

DIR=$1
WORKFLOW=$2
YAML=$3

echo $DIR

if [ ! -d $DIR ]; then
  virtualenv $DIR
  source $DIR/bin/activate
  pip install --upgrade setuptools
  pip install --upgrade arvados-cwl-runner
  ./acr.py $WORKFLOW $YAML
fi

if [ -d $DIR ]; then
  source $DIR/bin/activate
  ./acr.py $WORKFLOW $YAML
fi
