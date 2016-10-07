#!/bin/bash

DIR=$1
CLUSTER=$2
WORKFLOW=$3
YAML=$4

source /home/bcosc/.bashrc
arvswitch $CLUSTER

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
