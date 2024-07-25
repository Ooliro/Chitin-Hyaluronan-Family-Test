 #!/usr/bin/env sh

sed 's/\t/ /g' $1 > sedd.temp;
awk '{freq[$1]+=$NF} END {for (clade in freq) print clade, freq[clade]}' sedd.temp > grf.temp;
sed 's/ /\t/g' grf.temp > grf.csv

# Cleaning

rm grf.temp
rm sedd.temp
