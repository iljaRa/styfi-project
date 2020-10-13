#!/bin/bash

cd ~/git_repos/cv-sift-search/;

rm results.txt

IMAGE=$1

python3 searchengine.py $IMAGE;

cat results.txt
