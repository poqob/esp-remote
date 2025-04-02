#!/bin/bash
lftp  $1 -e "mirror -R $PWD/ /; quit"
#echo $PWD/