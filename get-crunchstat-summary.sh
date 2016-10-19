#!/bin/bash

source ~/.bashrc
UUID=$1
echo $UUID
CLUSTER=${UUID:0:5}
arvswitch $CLUSTER
echo $UUID
source ~/cs1/bin/activate
if [ ! -d ~/crunchstat_summaries/$UUID ]; then
  mkdir ~/crunchstat_summaries/$UUID
fi

if [[ $UUID =~ d1hrv ]]; then
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format html > ~/crunchstat_summaries/$UUID/$UUID.html
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format text > ~/crunchstat_summaries/$UUID/$UUID.txt
fi

if [[ $UUID =~ 8i9sb ]]; then
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format html > ~/crunchstat_summaries/$UUID/$UUID.html
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format text > ~/crunchstat_summaries/$UUID/$UUID.txt
fi

scp -r -P12345 ~/crunchstat_summaries/$UUID/ 127.0.0.1:/home/bcosc/crunchstat_summaries/
