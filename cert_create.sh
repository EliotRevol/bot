#!/bin/bash
#docker run -it --rm -p 80:80 -p 443:443  -v "$PWD"/certs:/etc/letsencrypt certbot/certbot certonly --email ali.yesilkanat@inria.fr --agree-tos  --no-eff-email  -d elections.audits.eu.org -d elections.whosban.eu.org
docker run -it --rm -p 80:80 -p 443:443  -v "$PWD"/certs:/etc/letsencrypt certbot/certbot certonly --email ali.yesilkanat@inria.fr --agree-tos  --no-eff-email  -d halflife.audits.eu.org
