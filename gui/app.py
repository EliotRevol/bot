import collections
import datetime
import functools
import glob
import logging
import operator
import os

from flask import Flask, render_template, request
from flask_basicauth import BasicAuth

from core.src import config
from core.src.utils import read_json, read_pickle
from gui.src.plots import title_welcome_fetch, transcript_welcome_walk_over_time, title_welcome_fetch_over_time

app = Flask(__name__)
app.config['BASIC_AUTH_REALM'] = 'inria'
app.config['BASIC_AUTH_USERNAME'] = 'wideadmin'
app.config['BASIC_AUTH_PASSWORD'] = 'wide123'

os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
app.config['SECRET_KEY'] = 'de510f5d2b6e5fff7cd3acd6bd4636c7946f5083'
app.config['CUSTOM_STATIC_PATH'] = config.get_gui_output()
basic_auth = BasicAuth(app)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

log_path = "../logs/flask.log"
access_log_path = "../logs/access.log"
if os.path.exists("../experiments"):
    # local docker
    EXPERIMENTS_PATH = "../experiments/*/*"
elif "EXPERIMENTS_PATH" in os.environ:
    # local development
    EXPERIMENTS_PATH = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/*"
elif os.path.exists("../gui_data/files"):
    # production docker
    EXPERIMENTS_PATH = "../gui_data/files"
    log_path = "../logs/flask_prod.log"
    access_log_path = "../logs/access.log"
else:
    raise FileNotFoundError("No valid experiment folder")
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(log_path), logging.StreamHandler()])
logging.info("logging set successfully")
logging.info(f"Experiments path on {EXPERIMENTS_PATH}")

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

    access_logs.info(ip)
    return render_template('index.html', error=error)


# BEGIN CRONS - REGEN PLOTS
@app.route('/cron_plot_title_welcome_fetch', methods=['GET', 'POST'])
@basic_auth.required
def cron_plot_title_welcome_fetch():
    last_pull_date = request.args.get("last_pull_date")
    return title_welcome_fetch.generate_plots(
        EXPERIMENTS_PATH, last_pull_date)


@app.route('/cron_plot_transcript_welcome_walk_over_time', methods=['GET', 'POST'])
@basic_auth.required
def cron_plot_transcript_welcome_walk_over_time():
    return transcript_welcome_walk_over_time.generate_plots(
        EXPERIMENTS_PATH)


@app.route('/cron_plot_transcript_welcome_walk_over_time_abs_3days_window', methods=['GET', 'POST'])
@basic_auth.required
def cron_plot_transcript_welcome_walk_over_time_abs_3days_window():
    return transcript_welcome_walk_over_time.generate_plots(
        EXPERIMENTS_PATH, standardize=False)


@app.route('/cron_plot_title_welcome_fetch_over_time_abs_3days_window', methods=['GET', 'POST'])
@basic_auth.required
def cron_plot_title_welcome_fetch_over_time_abs_3days_window():
    return title_welcome_fetch_over_time.generate_plots(
        EXPERIMENTS_PATH, standardize=False)


# END CRONS - REGEN PLOTS
@app.route('/title_welcome_fetch', methods=['GET'])
def plot_title_welcome_fetch():
    path = config.get_path("gui_data/plot_data/welcome_title_ratio")
    files = glob.glob(path + "/*json")
    creation_timestamps = [a.split("__")[-1].split(".")[0] for a in files]
    filename = files[creation_timestamps.index(max(creation_timestamps))]
    json_data = read_json(filename)
    return {"data": json_data['candidates'], "date": filename.split("__")[0].split(os.path.sep)[-1].replace("_", "/"),
            "political_mention": json_data['political_mention'], "total_videos": json_data["total_videos"],
            "most_common_videos": json_data["most_common_videos"]}


@app.route('/csa_transcript_duration', methods=['GET'])
def plot_csa_transcript_duration():
    path = config.get_path("gui_data/plot_data/csa_title_search")
    files = glob.glob(path + "/*pkl")
    creation_timestamps = [a.split("__")[-1].split(".")[0] for a in files]
    json_data = read_pickle(files[creation_timestamps.index(max(creation_timestamps))])
    json_result = []
    logging.info(json_data)
    for candidate in json_data:
        json_result.append({"candidate": candidate, "source": "CSA", "ratio": json_data[candidate]["csa"] * 100})
        json_result.append(
            {"candidate": candidate, "source": "Youtube", "ratio": json_data[candidate]["youtube"] * 100})
    return {"data": json_result, "candidates": list(json_data.keys())}


@app.route('/transcript_welcome_walk_over_time_3days_window', methods=['GET'])
def plot_transcript_welcome_walk_over_time_3days_window():
    path = config.get_path("gui_data/plot_data/transcript_welcome_walk_over_time")
    files = glob.glob(path + "/*json")
    cand_dict_list = [read_json(a) for a in files]
    dates = [a.split("/")[-1].split(".")[0] for a in files]
    dates_revers = [datetime.datetime.strptime(date, "%d_%m_%Y").strftime("%Y%m%d") for date in dates]
    dates_sorted, cand_dict_list_sorted = (list(t) for t in
                                           zip(*sorted(zip(dates_revers, cand_dict_list))))
    result_json = []
    for i in range(1, len(dates_sorted) - 1):
        summed_dict = dict(functools.reduce(operator.add,
                                            map(collections.Counter,
                                                [cand_dict_list_sorted[j] for j in range(i - 1, i + 2)])))

        summed_dict = {k: v / 3 for k, v in summed_dict.items()}
        summed_dict['date'] = dates_sorted[i]
        for k in cand_dict_list_sorted[0].keys():
            if k not in summed_dict:
                summed_dict[k] = 0.001
            if summed_dict[k] == 0:
                summed_dict[k] = 0.001
        result_json.append(summed_dict)
        # for c in summed_dict.keys():
        #     result_json.append(
        #         {"candidate": c, "date": dates_sorted[i],
        #          "ratio": summed_dict[c]})

    # result_json = sorted(result_json, key=lambda d: d['date'])
    return {"data": result_json, "candidates": list(cand_dict_list_sorted[i].keys())}



@app.route('/plot_over_time_abs_3days_window', methods=['GET'])
def plot_over_time_abs_3days_window():
    plot_type = request.args.get("plot_type")  # either transcript or title
    if plot_type == "transcript":
        path = config.get_path("gui_data/plot_data/transcript_welcome_walk_over_time_abs")
    elif plot_type == "title":
        path = config.get_path("gui_data/plot_data/title_welcome_fetch_over_time_abs")
    else:
        raise NotImplementedError
    files = glob.glob(path + "/*json")
    cand_dict_list = [read_json(a) for a in files]
    dates = [a.split("/")[-1].split(".")[0] for a in files]
    dates_revers = [datetime.datetime.strptime(date, "%d_%m_%Y").strftime("%Y%m%d") for date in dates]
    dates_sorted, cand_dict_list_sorted = (list(t) for t in
                                           zip(*sorted(zip(dates_revers, cand_dict_list))))
    result_json = []
    for i in range(1, len(dates_sorted) - 1):
        summed_dict = dict(functools.reduce(operator.add,
                                            map(collections.Counter,
                                                [cand_dict_list_sorted[j] for j in range(i - 1, i + 2)])))

        summed_dict = {k: v / 3 for k, v in summed_dict.items()}
        summed_dict['date'] = dates_sorted[i]
        for k in cand_dict_list_sorted[0].keys():
            if k not in summed_dict:
                summed_dict[k] = 0.001
            if summed_dict[k] == 0:
                summed_dict[k] = 0.001
        result_json.append(summed_dict)
    return {"data": result_json, "candidates": list(cand_dict_list_sorted[i].keys())}


@app.route('/transcript_welcome_walk_over_time', methods=['GET'])
def plot_transcript_welcome_walk_over_time():
    path = config.get_path("gui_data/plot_data/transcript_welcome_walk_over_time")
    files = glob.glob(path + "/*json")
    cand_dict_list = [read_json(a) for a in files]
    dates = [a.split("/")[-1].split(".")[0] for a in files]
    result_json = []
    for date, cand_dict in zip(dates, cand_dict_list):
        for c in cand_dict.keys():
            result_json.append(
                {"candidate": c, "date": datetime.datetime.strptime(date, "%d_%m_%Y").strftime("%Y-%m-%d"),
                 "ratio": cand_dict[c]})
    result_json = sorted(result_json, key=lambda d: d['date'])
    return {"data": result_json, "candidates": list(cand_dict.keys())}


@app.route('/transcript_welcome_walk_over_time_tsv', methods=['GET'])
def plot_transcript_welcome_walk_over_time_tsv():
    path = config.get_path("gui_data/plot_data/transcript_welcome_walk_over_time")
    files = glob.glob(path + "/*json")
    cand_dict_list = [read_json(a) for a in files]
    dates = [a.split("/")[-1].split(".")[0] for a in files]
    result_json = []

    for date, cand_dict in zip(dates, cand_dict_list):
        res = {"date": datetime.datetime.strptime(date, "%d_%m_%Y").strftime("%Y%m%d")}
        res.update(cand_dict)
        # cand_dict["date"]=datetime.datetime.strptime(date, "%d_%m_%Y").strftime("%Y%m%d")
        result_json.append(res)

    result_json = sorted(result_json, key=lambda d: d['date'])
    return {"data": result_json, "candidates": list(cand_dict.keys())}


@app.route('/transcript_plot_checkbox', methods=['GET', 'POST'])
def test():
    error = ""
    return render_template('transcript_plot_checkbox.html', error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    logging.info("started hosting")
