#!/bin/bash

# Author: Nolan Rudolph

ARGS=2

if [ $# -ne "$ARGS" ]
then
	echo "You passed $#/$ARGS parameters."
	echo "Use $ sudo bash saturateTables.sh [TABLE NAMES] [END ITERATION]"
fi

tableNames=$1
fin=$2
cur=1

while [[ $cur -le $fin ]]; do
	mysqlimport -u root -ppassword --local --fields-terminated-by=, netflow "$tableNames$cur"
	cur=$(($cur+1))
done


