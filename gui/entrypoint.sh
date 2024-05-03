export PYTHONPATH=/
export PATH=/opt/conda/envs/bot-crawler/bin:$PATH
gunicorn --workers 3 --bind unix:/gui/gui.sock -m 007 -g www-data app:app --timeout 600 -D
nginx -g 'daemon off;'