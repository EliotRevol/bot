#!/bin/bash

archive_name=$(date +'%m_%d_%Y')
sp="/home/ayesilka/Development/bot-crawler/output/"
cd "$sp"
tar -czvf archives/"$archive_name".tar.gz \
  *.gz \
  *.json \
  *.csv \
  *.txt --remove-files
scp -P 2202 "$sp"archives/"$archive_name".tar.gz ali@37.187.9.31:/home/ali/backups/widenuc!!!Give machine name here!!!/

