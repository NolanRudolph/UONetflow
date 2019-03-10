#!/bin/bash

# Author: Nolan Rudolph

ARGS=4

if [ $# -ne "$ARGS" ]
then
	echo "You passed $#/$ARGS parameters."
	echo "Use $ sudo bash iteratoryReplace.sh [SCRIPT] [DESTINATION] [ITERATORY VARIABLE] [END ITERATION]"
fi

sql_script=$1
dest=$2
var=$3
fin=$4
segNum=1

while [[ $segNum -le $fin ]]; do
	{ cat $sql_script | sed "s/$var/$var$segNum/g"; } >> $dest
	segNum=$(($segNum+1))
	echo "" >> $dest
done

