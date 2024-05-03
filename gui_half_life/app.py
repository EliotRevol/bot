import datetime
import glob
import itertools
import json
import logging
import os
import random
import re
import time
from collections import OrderedDict, Counter
from threading import Thread

import numpy as np
from fastdist import fastdist
from flask import Flask, render_template, request, send_from_directory
from flask_basicauth import BasicAuth

from core.src import config
from core.src.bot import runJob
from core.src.channel_sniffer import get_or_load
from core.src.user_agent_generator import generate_user_agent_and_resolution
from core.src.utils import dump, read_json
from gui_half_life.src.helper import fetch_channel_name
from gui_half_life.src.utils import get_timestamp

os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
app = Flask(__name__)
app.config['BASIC_AUTH_REALM'] = 'inria'
app.config['BASIC_AUTH_USERNAME'] = 'wideadmin'
app.config['BASIC_AUTH_PASSWORD'] = 'wide123'
app.config['SECRET_KEY'] = 'de510f5d2b6e5fff7cd3acd6bd4636c7946f5083'
app.config['CUSTOM_STATIC_PATH'] = config.get_gui_output()
basic_auth = BasicAuth(app)
regex = re.compile(r'[\n\r\t]')
watchTime = 50000  # 3000
lang = "en"
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

if "PROD" not in os.environ:
    log_path = "../logs_half_life/flask.log"
    access_log_path = "../logs_half_life/access.log"
else:
    # production docker
    log_path = "../logs_half_life/flask_prod.log"
    access_log_path = "../logs_half_life/access.log"

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(log_path), logging.StreamHandler()])
logging.info("logging set successfully")

access_logs = logging.getLogger("access")
formatter = logging.Formatter('%(asctime)s : %(message)s')
fileHandler = logging.FileHandler(access_log_path)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
access_logs.setLevel(logging.INFO)
access_logs.addHandler(fileHandler)
access_logs.addHandler(streamHandler)


@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']

    # access_logs.info(ip)
    return render_template('index.html', error=error)


@app.route('/channelSniff', methods=['POST'])
def channelSniff():
    url = request.form['url']
    channel_name = fetch_channel_name(url)

    return {"channel_videos": get_or_load({"channel": channel_name, "id": url}, lang,
                                          None),
            "channel_name": channel_name, }


@app.route('/output/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=config.get_gui_output(), path=filename)


@basic_auth.required
@app.route('/generate_reference', methods=['POST'])
def generate_ref():
    alea = int(watchTime / 10)
    k = 5
    events = [
        '{"type": "fetch", "searchSelection":1}',
    ]
    data_json = runJob(events, generate_user_agent_and_resolution(), None)

    starts = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
               "searchTerm": regex.sub(" ", rvk["title"]), "tag":
                   "welcome"} for rvk in random.choices(data_json, k=k)]
    events = [
        '{"type": "fetch", "searchSelection":3}',
    ]
    for s in starts:
        events.append('{"type": "watchOne", "video_id": "' + s[
            "video_id"] + '", "searchTerm": "' + regex.sub(" ",
                                                           s[
                                                               "searchTerm"]) + '", "watchTime": ' +
                      str(watchTime) + ', "alea": ' + str(alea) + '}')
        events.append('{"type": "fetch", "searchSelection":3}')
    # try:
    #     walk_res = runJob(events, user_agent_resolution, None, None, None)
    Thread(target=run_mainstream_job, args=(events, generate_user_agent_and_resolution(), "reference"),
           daemon=True).start()

    return "started reference generation job"


@app.route('/calculate_mainstreams', methods=['GET', 'POST'])
def calculate_mainstreams():
    mainstream_res1 = read_json(config.get_path(f"gui_half_life_data/vectors/mainstream/mainstream-1655466768.json"))
    mainstream_res2 = read_json(config.get_path(f"gui_half_life_data/vectors/mainstream/mainstream-1655466759.json"))
    walk = read_json(config.get_path(f"gui_half_life_data/walks/personalization-JEAN-LUC MÉLENCHON-k_5_4992.json"))
    set([a['url'] for a in mainstream_res1 if a['type'] == 'homepage' and a['videoViewsNB'] == 0]).intersection(
        set([a['url'] for a in mainstream_res2 if a['type'] == 'homepage' and a['videoViewsNB'] == 0]))


@app.route('/calculate_distance', methods=['GET', 'POST'])
def calculate_distance():
    mainstream_res = list(itertools.chain(
        *[read_json(a) for a in glob.glob(config.get_path(f"gui_half_life_data/vectors/mainstream/*.json"))]))
    reference_res = list(itertools.chain(
        *[read_json(a) for a in glob.glob(config.get_path(f"gui_half_life_data/vectors/reference/*.json"))]))
    walk_res = read_json(
        config.get_path(f"gui_half_life_data/walks/personalization-JEAN-LUC MÉLENCHON-k_5_4992.json"))

    mainstream_videos = [a['url'] for a in mainstream_res if a['type'] == 'homepage']
    reference_videos = [a['url'] for a in reference_res if a['type'] == 'homepage']
    reference_videos_removed_ones = [a for a, b in Counter(reference_videos).items() if b > 1]
    mainstream_videos_removed_ones = [a for a, b in Counter(mainstream_videos).items() if b > 1]
    walk_videos = [a['url'] for a in walk_res if a['type'] == 'homepage']
    total_videos = set.union(set(mainstream_videos_removed_ones),
                             set(reference_videos_removed_ones), set(walk_videos))
    total_videos = OrderedDict.fromkeys(total_videos)
    welcome_vec = np.array([a in mainstream_videos_removed_ones for a in total_videos]).astype(float)
    # total_videos_vec=np.array(total_videos).astype(float)
    walk_distances = []
    reference_distances = []
    for i in range(6):
        ref_videos_iter = [a['url'] for a in reference_res if a['type'] == 'homepage' and a['videoViewsNB'] == i and a[
            'url'] in reference_videos_removed_ones]
        ref_videos_vec = np.array([a in ref_videos_iter for a in total_videos]).astype(float)

        walk_videos_iter = [a['url'] for a in walk_res if a['type'] == 'homepage' and a['videoViewsNB'] == i and a[
            'url']]
        walk_videos_vec = np.array([a in walk_videos_iter for a in total_videos]).astype(float)

        walk_distances.append(fastdist.cosine(welcome_vec, walk_videos_vec))
        reference_distances.append(fastdist.cosine(welcome_vec, ref_videos_vec))
    print(walk_distances)
    print(reference_distances)
    # mainstream_vector = [a in mainstream_videos for a in total_videos]
    # walk_vector = [a in walk_videos for a in total_videos]
    # reference_vector = [a in reference_videos for a in total_videos]

    # print(len(intersected_videos))
    print(len(walk_res))
    print(len(reference_videos))
    print(len(mainstream_videos))
    print(len(set(reference_videos).intersection(set(mainstream_videos))))
    print(len(set(reference_videos).intersection(set(walk_videos))))
    print(len(set(mainstream_videos).intersection(set(walk_videos))))

    return "OK"


@basic_auth.required
@app.route('/generate_mainstream', methods=['POST'])
def generate_mainstream():
    events = [
        '{"type": "fetch", "searchSelection":3}',  # TODO searchselection 3
    ]
    user_agent_resolution = generate_user_agent_and_resolution()

    Thread(target=run_mainstream_job, args=(events, user_agent_resolution, "mainstream"),
           daemon=True).start()

    return "started mainstream generation job"


def run_mainstream_job(events, user_agent_resolution, vector_name):
    res = runJob(events, user_agent_resolution, None, None, None)

    csv_path = dump(globals(), res,
                    vector_name + "-" + get_timestamp(), None, None, None, f"gui_half_life_data/vectors/{vector_name}")
    logging.info("Finished generation, path: " + csv_path)


@app.route('/walk_iter', methods=['POST'])
def walk_iter():
    time_time = time.time()
    channel_name = request.form['channel_name']
    channel_videos = request.form['channel_videos']
    channel_videos = json.loads(channel_videos)
    alea = int(watchTime / 10)
    k = 5

    starts = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
               "searchTerm": regex.sub(" ", rvk["title"]), "tag":
                   channel_name} for rvk in random.choices(channel_videos, k=k)]
    events = [
        '{"type": "fetch", "searchSelection":3}',
    ]
    for s in starts:
        events.append('{"type": "watchOne", "video_id": "' + s[
            "video_id"] + '", "searchTerm": "' + regex.sub(" ",
                                                           s[
                                                               "searchTerm"]) + '", "watchTime": ' +
                      str(watchTime) + ', "alea": ' + str(alea) + '}')
        events.append('{"type": "fetch", "searchSelection":3}')
    user_agent_resolution = generate_user_agent_and_resolution()
    try:
        walk_res = runJob(events, user_agent_resolution, None, None, None)
    except Exception as e:
        logging.exception("Error while calling bot docker")
        raise e
    csv_path = dump(globals(), walk_res,
                    "personalization-" + channel_name + "-" + "k_" + str(k) + "_" + str(
                        random.randint(1, 10000)), None, None, None, f"gui_half_life_data/walks")

    def load_latest_jsons(regex_path):
        return list(itertools.chain(
            *[read_json(a) for a in glob.glob(config.get_path(regex_path)) if
              int(os.path.basename(a).split("-")[1].split(".")[0]) > int(
                  round((datetime.datetime.now() + datetime.timedelta(days=-1)).timestamp()))]))

    mainstream_res = load_latest_jsons("gui_half_life_data/vectors/mainstream/*.json")
    reference_res = load_latest_jsons("gui_half_life_data/vectors/reference/*.json")

    for a in mainstream_res:
        a['url'] = a['url'].replace("https://www.youtube.com/watch?v=", "")
    for a in reference_res:
        a['url'] = a['url'].replace("https://www.youtube.com/watch?v=", "")

    mainstream_videos = [a['url'] for a in mainstream_res if a['type'] == 'homepage']
    reference_videos = [a['url'] for a in reference_res if a['type'] == 'homepage']
    reference_videos_removed_ones = [a for a, b in Counter(reference_videos).items() if b > 1]
    mainstream_videos_removed_ones = [a for a, b in Counter(mainstream_videos).items() if b > 1]
    walk_videos = [a['url'] for a in walk_res if a['type'] == 'homepage']
    total_videos = set.union(set(mainstream_videos_removed_ones),
                             set(reference_videos_removed_ones), set(walk_videos))
    total_videos = OrderedDict.fromkeys(total_videos)
    welcome_vec = np.array([a in mainstream_videos_removed_ones for a in total_videos]).astype(float)
    # total_videos_vec=np.array(total_videos).astype(float)
    distances = []
    # reference_distances = []
    for i in range(6):
        ref_videos_iter = [a['url'] for a in reference_res if a['type'] == 'homepage' and a['videoViewsNB'] == i and a[
            'url'] in reference_videos_removed_ones]
        ref_videos_vec = np.array([a in ref_videos_iter for a in total_videos]).astype(float)

        walk_videos_iter = [a['url'] for a in walk_res if a['type'] == 'homepage' and a['videoViewsNB'] == i]
        walk_videos_vec = np.array([a in walk_videos_iter for a in total_videos]).astype(float)

        walk_dist = fastdist.cosine(welcome_vec, walk_videos_vec)
        ref_dist = fastdist.cosine(welcome_vec, ref_videos_vec)
        distances.append({"type": "Reference", "step": i, "value": ref_dist})
        distances.append({"type": "Walk", "step": i, "value": walk_dist})

    result = {"videos": starts, "csv_path": config.get_gui_rel_output(csv_path), "distances": distances}
    logging.info(result)
    # result = {'videos': [
    #     {'video_id': 'Pbel051H7-s', 'searchTerm': 'The Best Electric Temperature Controlled Gooseneck Kettles',
    #      'tag': 'James Hoffmann'},
    #     {'video_id': 'P-Ga8SRhRrE', 'searchTerm': 'Why Cheap Coffee Makers Suck (And How To Fix Them)',
    #      'tag': 'James Hoffmann'},
    #     {'video_id': 'FL65i1XhVec', 'searchTerm': 'The Weber HG-2 - The $1,650 Hand Grinder', 'tag': 'James Hoffmann'},
    #     {'video_id': 'IW8j1nNe5xk', 'searchTerm': 'Sour Candy Espresso #Shorts', 'tag': 'James Hoffmann'},
    #     {'video_id': 'P-Ga8SRhRrE', 'searchTerm': 'Why Cheap Coffee Makers Suck (And How To Fix Them)',
    #      'tag': 'James Hoffmann'}], 'csv_path': '../output/personalization-James Hoffmann-k_2_2151.csv'}
    logging.info("Took time: " + str(time.time() - time_time))
    # result={'videos': [{'video_id': 'vdxHe12lUmI', 'searchTerm': 'Meeting immersif de Jean-Luc Mélenchon à Nantes', 'tag': 'JEAN-LUC MÉLENCHON'}, {'video_id': 'DGzlFcxYnX4', 'searchTerm': 'Héritage : au-delà de 12 millions deuros, je donne tout aux jeunes !', 'tag': 'JEAN-LUC MÉLENCHON'}, {'video_id': '2FCQBgx7Sho', 'searchTerm': 'Docu #9 : Les coulisses du déplacement aux Antilles', 'tag': 'JEAN-LUC MÉLENCHON'}, {'video_id': 'j8f8iLh3tB8', 'searchTerm': 'Je veux empêcher le recul de la France 🇫🇷', 'tag': 'JEAN-LUC MÉLENCHON'}, {'video_id': '-XLXIeyi-oQ', 'searchTerm': 'Taïwan : je refuse la guerre froide avec la Chine', 'tag': 'JEAN-LUC MÉLENCHON'}], 'csv_path': '../gui_half_life_data/walks/personalization-JEAN-LUC MÉLENCHON-k_5_96.csv', 'distances': [{'type': 'Reference', 'step': 0, 'value': 0.6354501362538935}, {'type': 'Walk', 'step': 0, 'value': 0.38129905401871683}, {'type': 'Reference', 'step': 1, 'value': 0.2636410942419923}, {'type': 'Walk', 'step': 1, 'value': 0.14245535304298249}, {'type': 'Reference', 'step': 2, 'value': 0.2605544905058995}, {'type': 'Walk', 'step': 2, 'value': 0.11028801525908322}, {'type': 'Reference', 'step': 3, 'value': 0.2614064523559687}, {'type': 'Walk', 'step': 3, 'value': 0.13125160220218882}, {'type': 'Reference', 'step': 4, 'value': 0.266832911963873}, {'type': 'Walk', 'step': 4, 'value': 0.1378142708904486}, {'type': 'Reference', 'step': 5, 'value': 0.26516827988219116}, {'type': 'Walk', 'step': 5, 'value': 0.10709264535133534}]}

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    logging.info("started hosting")
