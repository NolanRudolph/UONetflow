#!/bin/bash

# Author: Nolan Rudolph

for f in *.csv; do
	dest="${f%%.*}"
	mv $f $dest
done

