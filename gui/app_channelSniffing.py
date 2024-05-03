import json
import os
import random
import re

import flask_login
from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from flask_login import UserMixin, LoginManager

import logging

from core.src import config
from core.src.bot import runJob
from core.src.channel_sniffer import get_or_load
from core.src.user_agent_generator import generate_user_agent_and_resolution
from core.src.utils import dump
from gui.src.auth import Auth
from gui.src.helper import fetch_channel_name

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler("../logs/flask.log"), logging.StreamHandler()])
logging.info("sucessfully import libs")
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'de510f5d2b6e5fff7cd3acd6bd4636c7946f5083'
app.config['CUSTOM_STATIC_PATH'] = config.get_gui_output()
regex = re.compile(r'[\n\r\t]')
watchTime = 30000
login_manager = LoginManager()
login_manager.init_app(app)
logging.info("set flask login manager")
lang = "en"

auth = Auth()
logging.info("set redis auth sucessfully")


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if auth.check_user(username):
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if auth.check_user(username):
        return
    user = User()
    user.id = username
    # user.is_authenticated = request.form['pw'] == users[username]['pw']
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    if request.method == 'POST':
        username = request.form.get('username')

        if auth.check_user_password(username, request.form.get("pw")):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('walk'))
        else:
            error = "Username or password do not match."

    return render_template('login.html', error=error)


@app.route('/walk')
@flask_login.login_required
def walk():
    return render_template('walk.html')


@app.route('/channelSniff', methods=['POST'])
def channelSniff():
    url = request.form['url']
    channel_name = fetch_channel_name(url)

    return {"channel_videos": get_or_load({"channel": channel_name, "id": url.replace("http://youtube.com", "")}, lang,
                                          None),
            "channel_name": channel_name, }


@app.route('/output/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=config.get_gui_output(), path=filename)


@app.route('/walk_iter', methods=['POST'])
def walk_iter():
    channel_name = request.form['channel_name']
    channel_videos = request.form['channel_videos']
    channel_videos = json.loads(channel_videos)
    alea = int(watchTime / 10)
    k = 2
    rvk = random.choice(channel_videos)
    s = {"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
         "searchTerm": regex.sub(" ", rvk["title"]), "tag":
             channel_name}

    search_term = regex.sub(" ", s["searchTerm"])
    events = [
        # remove from gi alea 5 seconds
        '{"type": "watchOne", "video_id": "' + s[
            "video_id"] + '", "searchTerm": "' + search_term + '", "watchTime": ' + str(watchTime) + ', "alea": ' + str(
            alea) + '}',
        '{"type": "fetchAutoplay", "searchSelection": ' + str(k) + ', "watchTime":  ' + str(alea) + ' }',
        '{"type": "fetch", "searchSelection":3}'
    ]

    user_agent_resolution = generate_user_agent_and_resolution()
    try:
        res = runJob(events, user_agent_resolution, None, None, None)
    except Exception as e:
        logging.exception("Error while calling bot docker")
        raise e
    csv_path = dump(globals(), res,
                    "autoplay-k-" + channel_name + "-" + s["tag"] + "_" + str(k) + "_" + str(
                        random.randint(1, 10000)), None, None, None)

    return {"search_term": search_term, "csv_path": config.get_gui_rel_output(csv_path)}
    # time.sleep(1)
    # return {'search_term': 'PRIMARK ⎮ Maquillage à 2€, 3€... Ça vaut le coup ?!',
    #         'csv_path': './output/autoplay-k-Le monde de Salomé-Le monde de Salomé_2_6306.csv',
    #         'channel_name': channel_name}   # TODO Only for debug


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    logging.info("started hosting")
