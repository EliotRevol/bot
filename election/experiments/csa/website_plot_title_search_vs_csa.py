import datetime
import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

from csa.extract_from_csa_data import get_time
from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_multi_folder, dump_pickle


def title_check(candidates_list, titles, experiment_type, plot_title=""):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        candidate_dictionary[candidate] += len(
            [a for a in titles if check_with_accent(candidate_lower, a.lower())])
    print(candidate_dictionary)
    plt.figure(figsize=(10, 5))

    plot_title_combined = f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion

    values = candidate_dictionary.values()
    plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
    plt.xticks(rotation=90)
    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    plt.savefig("../../plots/csa/transcript_search/" + file_name + ".png")


if __name__ == '__main__':

    experiment_folder = ["14.01.2022", "01_*",'02_*',
                         "03_01_2022",
                         "03_02_2022",
                         "03_03_2022",
                         "03_04_2022",
                         "03_05_2022",
                         "03_06_2022"

                         ]
    # experiment_folder = ["14.01.2022", "07_01_2022"]
    # csa = pd.read_csv("pres_2022.csv")
    CAND = Candidates.official
    # csa['total_time'] = csa[["time_candidat", "time_support", "time_mention"]].sum(axis=1)
    # csa_dict = {}
    # for candidate in CAND:
    #     for _, t in csa.groupby("candidat")['total_time'].sum().reset_index().iterrows():
    #         if check_with_accent(candidate, t['candidat']):
    #             csa_dict[candidate] = t['total_time']

    csa_df = pd.read_csv("TP-TA_Presidentielle_2022__1er janvier au 7 mars 2022.csv", sep=";",
                         encoding="ISO-8859-1", header=None,
                         names=["Channel", "_", "Candidat", "Type", "Duration", "ratio"])

    csa_df = csa_df[csa_df.Type.isin(["Candidat", "Soutiens", "Antenne"])]
    csa_df['Hours'] = csa_df.Duration.apply(lambda x: get_time(x))
    # experiment_folder = ["14.01.2022", "07_01_2022"]
    csa_df = csa_df.groupby("Candidat").sum("Hours").reset_index()
    csa_dict = {}
    for candidate in CAND:
        cand_df = csa_df[csa_df.Candidat.apply(lambda x: check_with_accent(candidate.lower(), x.lower()))]
        csa_dict[candidate] = cand_df.Hours.iloc[0]

    csa_dict = {k: {"csa": v / sum(csa_dict.values()) if sum(csa_dict.values()) > 0 else 0} for k, v in
                csa_dict.items()}

    experiments_json = read_multi_folder(experiment_folder, Experiments.WELCOME_FETCH, ResultTypes.JSON,
                                         "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/")
    # url_tag_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}

    video_titles = [b['title'] for e in experiments_json for b in e]
    # Polls
    candidate_dictionary = defaultdict.fromkeys(CAND, 0)
    for candidate1 in tqdm(candidate_dictionary.keys()):
        candidate_lower = candidate1.lower()
        durations = sum(
            [1 for text in video_titles if check_with_accent(candidate_lower, text.lower())])
        candidate_dictionary[candidate1] += durations
    print(candidate_dictionary)
    plt.figure(figsize=(10, 5))
    plot_title_combined = f"{Experiments.WELCOME_WALK}-Candidates From Polls"
    plt.title(plot_title_combined)  # enum to string converion
    values = candidate_dictionary.values()
    plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
    for c, v in candidate_dictionary.items():
        csa_dict[c]['youtube'] = v / sum(values) if sum(values) > 0 else 0
    dump_pickle(
        f"title_search_csa_dict_01-01__07-03_{int(datetime.datetime.timestamp(datetime.datetime.now()))}.pkl",
        csa_dict)
