export PYTHONPATH=/
export PATH=/opt/conda/envs/bot-crawler/bin:$PATH
export PROD=True
gunicorn --workers 3 --bind unix:/gui_half_life/gui_half_life.sock -m 007 -g www-data app:app --timeout 6000000 -D
nginx -g 'daemon off;'