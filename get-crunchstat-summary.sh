#!/bin/bash

source ~/.bashrc
arvswitch $2

source ~/cs1/bin/activate
if [ ! -d ~/crunchstat_summaries/$1 ]; then
  mkdir ~/crunchstat_summaries/$1
fi

~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $1 --format html > ~/crunchstat_summaries/$1/$1.html
~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $1 --format text > ~/crunchstat_summaries/$1/$1.txt

scp -r -P12345 ~/crunchstat_summaries/$1/ 127.0.0.1:/home/bcosc/crunchstat_summaries/
