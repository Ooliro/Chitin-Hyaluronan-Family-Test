#!/bin/bash

head -100 $1 | cut -f11 | grep -o "\[.*\]" | sed 's/\[//g;s/\]//g' | awk '{print $1,$2}' | sort | uniq > names.txt
