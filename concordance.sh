#!/bin/bash

CUROVERSEDIR=$1
VERITASDIR=$2

for FILE in `find $1 -name 'Sample*'`
do
  BASE=`basename $FILE`
  sort -k 1,1 $1/$BASE -o $1/$BASE
  sort -k 1,1 $2/$BASE -o $2/$BASE
  echo $BASE
  echo "Variant Count" `wc -l $1/$BASE | cut -f1 -d' '` `wc -l $2/$BASE | cut -f1 -d' '`
  CVARS=`cat $1/$BASE | cut -f 3`
  VVARS=`cat $2/$BASE | cut -f 3`
  echo $CVARS
  echo $VVARS
  echo `diff <( echo "$CVARS" ) <( echo "$VVARS" )`
done
