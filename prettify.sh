#!/bin/bash

for filename in ./data/*/*;

do
    python -m json.tool $filename >> $filename.tmp;
    mv -f $filename.tmp $filename; 
    echo $filename;

done;