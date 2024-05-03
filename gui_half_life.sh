#!/bin/bash
#
## run redis container if not working
#if [ ! "$(docker ps -q -f name=redis-instance)" ]; then
#  docker run --rm --name redis-instance -d -p 6379:6379 -v $PWD/gui/redis.conf:/redis.conf -v $PWD/gui/redis_data:/data/ redis /redis.conf
#fi
##build gui
#docker image build -f Dockerfile -t gui .
## kill working gui-instance container if working
#if [ "$(docker ps -q -f name=gui-instance)" ]; then
#  docker rm -f gui-instance
#fi
#redis_ip="$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-instance)"
##run gui
#docker run --rm --name gui-instance -p 5000:5000 -v /run/user/"$(id -u)"/docker.sock:/var/run/docker.sock -v $PWD/input:/input -v $PWD/output:/output -v $PWD/bot-inputs:/bot-inputs -v $PWD/logs:/logs -e REDIS_URL="$redis_ip" -e COOKIES=$PWD/core/cookies -d gui

#build gui
docker image build -f Dockerfile_half_life -t gui-half-life .
# kill working gui-instance container if working
if [ "$(docker ps -q -f name=gui-half-life-instance)" ]; then
  docker rm -f gui-half-life-instance
fi

#docker run --rm --name gui-instance -p 80:80 -v $PWD/gui_data:/gui_data -v $PWD/logs:/logs -d  gui
#docker run --rm --name gui-instance -p 80:80 -p 443:443 -v $PWD/gui_data:/gui_data -v $PWD/logs:/logs -v /home/ayesilka/Development/bot-crawler/certs:/etc/letsencrypt -d  gui


# for nuc production
#docker run --rm --name gui-half-life-instance -p 80:80 -p 443:443 -v $PWD/gui_half_life_data:/gui_half_life_data -v $PWD/logs_half_life/flask_logs:/logs -v $PWD/logs_half_life/nginx_logs:/var/log/nginx -v /home/ayesilka/Development/bot-crawler/certs:/etc/letsencrypt -d  gui-half-life

# for local below
#docker run --rm --name gui-half-life-instance -p 80:5000 -v $PWD/gui_half_life_data:/gui_half_life_data -v $PWD/logs_half_life/flask_logs:/logs  -v $PWD/logs_half_life/nginx_logs:/var/log/nginx -v /var/run/docker.sock:/var/run/docker.sock --user $(id -u):$(id -g) -d gui-half-life




# docker run --rm --name gui-half-life-instance -p 80:80 -p 443:443 -v $PWD/gui_half_life_data:/gui_half_life_data -v $PWD/logs_half_life/flask_logs:/logs_half_life -v $PWD/logs_half_life/nginx_logs:/var/log/nginx -it  gui-half-life /bin/bash
#docker run --rm --name gui-half-life-instance -p 8085:8085 -p 443:443 -v $PWD/gui_half_life_data:/gui_half_life_data -v $PWD/logs_half_life/flask_logs:/loglf_life -v $PWD/logs_half_life/nginx_logs:/var/log/nginx -v /run/user/"$(id -u)"/docker.sock:/var/run/docker.sock -d  gui-half-life

docker run --rm --name gui-half-life-instance -p 8085:8085 -v $PWD/gui_half_life_data:/gui_half_life_data -v $PWD/logs_half_life/flask_logs:/logs_half_life  -v $PWD/logs_half_life/nginx_logs:/var/log/nginx -v /run/user/"$(id -u)"/docker.sock:/var/run/docker.sock -d gui-half-life





