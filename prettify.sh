#!/bin/bash

for filename in ./data/event/*;

do
    python -m json.tool $filename >> $filename.tmp;
    mv -f $filename.tmp $filename; 
    echo $filename;

done;

for filename in ./data/schema/*;

do
    python -m json.tool $filename >> $filename.tmp;
    mv -f $filename.tmp $filename; 
    echo $filename;

done;