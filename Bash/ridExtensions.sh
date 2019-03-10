for f in *.csv; do
	dest="${f%%.*}"
	mv $f $dest
done

