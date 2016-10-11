#!/bin/bash

# Make sure to add this directory to PATH in .bashrc

DIR=$1
CLUSTER=$2
WORKFLOW=$3
YAML=$4

if [ "$1" == "-h" ]; then
  echo "Usage: run-acr.sh directory_name cluster_uuid workflow_path yaml_path"
  exit 0
fi

if [ "$1" == "" ]; then
  echo "Usage: run-acr.sh directory_name cluster_uuid workflow_path yaml_path"
  exit 0
fi

source /home/bcosc/.bashrc
arvswitch $CLUSTER

if [ ! -d $DIR ]; then
  virtualenv $DIR
  source $DIR/bin/activate
  pip install --upgrade setuptools
  pip install --upgrade arvados-cwl-runner
fi

source $DIR/bin/activate
UUID=`acr.py $WORKFLOW $YAML`
echo $UUID
TRIM_UUID=${UUID% *}
echo $TRIM_UUID
get-crunchstat-summary.sh $TRIM_UUID $CLUSTER
