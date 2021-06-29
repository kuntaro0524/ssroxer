#!/bin/bash

i=5

 i=$((i-1))
 n=$((i/100+1))
 j=$((i%100))

 echo $n $j
 #printf "$root/$data/${prefix}_data_%.6d.h5 //%d\n" $n $j >> hits_${prefix}.lst

