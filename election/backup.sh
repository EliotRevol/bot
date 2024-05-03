#!/bin/bash

archive_name=$(date +'%m_%d_%Y')
sp="/home/ayesilka/Development/bot-crawler/output/"
cd "$sp"
tar -czvf archives/"$archive_name".tar.gz \
  *.gz \
  *.json \
  *.csv \
  *.txt --remove-files
scp -P 2202 "$sp"archives/"$archive_name".tar.gz ali@37.187.9.31:/home/ali/backups/widenuc4/






mkdir /home/ayesilka/Development/bot-crawler/output/archives
mkdir /home/ayesilka/Development/bot-crawler/backup
nano /home/ayesilka/Development/bot-crawler/backup/backup.sh
crontab -e
0 2 * * * /bin/bash /home/ayesilka/Development/bot-crawler/backup/backup.sh >> /home/ayesilka/Development/bot-crawler/backup/backup.log 2>&1



1
3
4





scp -P 2202 -r  ali@37.187.9.31:/home/ali/backups /home/ali/Development/election/
for file in *.tar.gz; do tar xzvf "${file}" --one-top-level && rm "${file}"; done



