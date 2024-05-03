#Dockerfile for GUI
FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get install nginx -y

SHELL ["/bin/bash", "--login", "-c"]
ADD environment.yml /
RUN conda env create -f environment.yml
#RUN  apt-get install docker.io -q -y
#RUN docker --version # to check if docker is installed correctly
EXPOSE 5000

ENV PYTHONPATH=/
COPY gui /gui
COPY core /core
COPY bot /bot



ENV PATH /opt/conda/envs/bot-crawler/bin:$PATH
#ENTRYPOINT ["python", "app.py"]
RUN usermod $(id -un) -g www-data
# install gunicorn -> need for yaml export and force build first
#ADD gui/nginx_config/gui.service /etc/systemd/system/
ADD gui/nginx_config/gui /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/gui /etc/nginx/sites-enabled
RUN rm /etc/nginx/sites-enabled/default

#RUN /opt/conda/envs/bot-crawler/bin/gunicorn --workers 3 --bind unix:/gui/gui.sock -m 007 -g www-data app:app -D
WORKDIR /gui
#ADD gui/entrypoint.sh
ENTRYPOINT ["/bin/bash","/gui/entrypoint.sh"]
#
#
#RUN systemctl start gui
#RUN systemctl enable gui
#RUN systemctl status gui
##RUN ufw allow 'Nginx Full'
#WORKDIR /gui
#RUN systemctl start nginx