import datetime
import glob
import logging
import os.path
from collections import Counter

import numpy as np
from tqdm import tqdm

from core.src.config import get_path
from core.src.utils import dump_json, read_json
from gui.src.plots.consts import ResultTypes, Experiments, Candidates, LegislativeParties
from gui.src.utils import check_with_accent, multi_check_with_accent


def parse_filename_to_date(filename):
    return parse_filename(filename).strftime("%d_%m_%Y")


def parse_filename(filename):
    return datetime.datetime.fromtimestamp(int(filename.split("-")[-1].replace(".json", "")))


def parse_filename_to_timestamp(filename):
    return parse_filename(filename).timestamp()


def generate_plots(experiment_files_path, standardize=True):
    files = [a for a in glob.glob(os.path.join(experiment_files_path, "*")) if
             Experiments.NATIONAL_NEWS_FETCH in a and ResultTypes.JSON in a]
    dates = set([parse_filename_to_date(a) for a in files])
    dates = set([a for a in dates if a.split("_")[-1] == '2022'])
    now = datetime.datetime.now()
    dates_to_remove = [now, now + datetime.timedelta(days=-1), now + datetime.timedelta(days=-2),
                       now + datetime.timedelta(days=1), now + datetime.timedelta(days=2)]
    for d in dates_to_remove:
        dates.discard(d.strftime("%d_%m_%Y"))  # need to remove today

    if standardize:
        path_for_jsons = "gui_data/plot_data/legislative_title_welcome_fetch_over_time/*.json"
    else:
        path_for_jsons = "gui_data/plot_data/legislative_title_welcome_fetch_over_time_abs/*.json"
    for a in glob.glob(get_path(path_for_jsons)):
        dates.discard(a.split("/")[-1].split(".")[0])
    if len(dates) > 0:
        dates_strp = [datetime.datetime.strptime(a, "%d_%m_%Y") for a in dates]
        experiments = []
        min_ts = (min(dates_strp) + datetime.timedelta(days=-3)).timestamp()
        max_ts = (max(dates_strp) + datetime.timedelta(days=3)).timestamp()
        for f in files:
            # Reading files only from the date range we need to make efficient implementation
            if min_ts < parse_filename_to_timestamp(f) < max_ts:
                try:
                    experiments.append(([b['title'] for b in read_json(f)], f))
                except:
                    logging.error("Exception on reading file: " + f)

        valid_exps_dates = [(experiments[i][0], parse_filename_to_date(experiments[i][1])) for i in
                            range(len(experiments)) if
                            len(experiments[i][0]) > 0]

        result_date_dict = {a: {b: 0 for b in LegislativeParties.Parties} for a in dates}
        if len(result_date_dict) > 0:
            for exp, date in tqdm(valid_exps_dates):
                if date in result_date_dict:
                    for candidate,snonyms in LegislativeParties.Parties.items():
                        # video_titles = [(exp['text'], exp['duration']) for e in exp for exp in e['transcript']]

                        title_count = sum(
                            [1 for title in exp if
                             multi_check_with_accent([candidate] + snonyms, title.lower())])
                        result_date_dict[date][candidate] += title_count
        # with open("temp_transcript.pkl", "wb") as f:
        #     pickle.dump(result_date_dict, f)
        for date in result_date_dict.keys():
            values = np.array(list(result_date_dict[date].values()))
            if standardize:
                std = np.std(values)
                values = (values - np.mean(values)) / std if std != 0 else values
            result_date_dict[date] = {k: v for k, v in zip(result_date_dict[date].keys(), values.tolist())}
            if standardize:
                output = get_path(
                    f"gui_data/plot_data/legislative_title_welcome_fetch_over_time/{date}.json")
            else:
                output = get_path(
                    f"gui_data/plot_data/legislative_title_welcome_fetch_over_time_abs/{date}.json")
            dump_json(result_date_dict[date], output)
    return "processed " + str(len(dates)) + " dates"
    # experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON)

    # experiments = read_experiments("../../07_01_2022", exp, ResultTypes.JSON)

    # experiments = [x for x in experiments if x]  # remove empty lists
    # video_titles = [f['title'].lower() for e in experiments for f in e if f]


if __name__ == '__main__':
    os.environ['BASE_DIRECTORY'] = os.path.dirname("/home/ali/Development/bot-crawler/")

    generate_plots("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/05_*", standardize=False)
