#!/bin/bash



/usr/bin/curl --max-time 60000000 -X POST -u wideadmin:wide123 https://elections.whosban.eu.org/generate_reference
/usr/bin/curl --max-time 60000000  -X POST -u wideadmin:wide123 https://elections.whosban.eu.org/generate_mainstream
echo "Finished scripts for regeneration"





