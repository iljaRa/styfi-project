#!/bin/bash

cd ~/git_repos/cv-sift-search/;

IMAGE=$1
RESPONSEPATH=$2

python3 searchengine.py $IMAGE $RESPONSEPATH 

#cat $RESPONSEPATH;

rm $IMAGE;
#rm $RESPONSEPATH;
