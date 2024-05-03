#!/bin/bash


export LAST_PULL_DATE=$(tail -n 1 /home/ayesilka/Development/bot-crawler/gui_data/dates_pull.txt)
echo "Fetching new data $LAST_PULL_DATE"
for nuc_number in 1 2 3 4 5
do
  for file in $(ssh -p 2202 ali@37.187.9.31 "cd backups/widenuc$nuc_number; ls [0-9]* | awk -F '.' '{if (\$1 > \"$LAST_PULL_DATE\") print \$0}'")
  do
    scp -r -P 2202 -v ali@37.187.9.31:/home/ali/backups/widenuc$nuc_number/$file /home/ayesilka/Development/bot-crawler/gui_data/backups/widenuc$nuc_number/$file
  done
done
ls /home/ayesilka/Development/bot-crawler/gui_data/backups/* | cut -d'/' -f 1 | cut -d'.' -f 1 | sort -nr | head -n1 >> /home/ayesilka/Development/bot-crawler/gui_data/dates_pull.txt

cd /home/ayesilka/Development/bot-crawler/gui_data/files
for file in /home/ayesilka/Development/bot-crawler/gui_data/backups/*/*.gz; do tar xzf "${file}" && rm "${file}"; done

/usr/bin/curl --max-time 6000 -u wideadmin:wide123 https://elections.whosban.eu.org/cron_plot_title_welcome_fetch?last_pull_date=$LAST_PULL_DATE
/usr/bin/curl --max-time 6000 -u wideadmin:wide123 https://elections.whosban.eu.org/cron_plot_transcript_welcome_walk_over_time_abs_3days_window
/usr/bin/curl --max-time 6000 -u wideadmin:wide123 https://elections.whosban.eu.org/cron_plot_title_welcome_fetch_over_time_abs_3days_window
echo "Finished scripts for regeneration"





