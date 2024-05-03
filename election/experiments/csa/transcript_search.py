import glob
import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_transcript, read_multi_folder


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
    experiment_folder = ["14.01.2022", "07_01_2022"]
    csa = pd.read_csv("pres_2022.csv")
    csa['total_time'] = csa[["time_candidat", "time_support", "time_mention"]].sum(axis=1)
    csa_dict = {}
    for candidate in Candidates.polls:
        for _, t in csa.groupby("candidat")['total_time'].sum().reset_index().iterrows():
            if check_with_accent(candidate, t['candidat']):
                csa_dict[candidate] = t['total_time']
    csa_dict = {k: {"csa": v / sum(csa_dict.values()) if sum(csa_dict.values()) > 0 else 0} for k, v in
                csa_dict.items()}
    for exp in [Experiments.WELCOME_WALK,
                Experiments.NATIONAL_NEWS_WALK]:
        experiments_json = read_multi_folder(experiment_folder, exp, ResultTypes.TRANSCRIPT)
        url_tag_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}

        video_titles = ["".join(exp['text']).lower() for e in experiments_json for exp in e['transcript']]
        # Polls
        candidate_dictionary = defaultdict.fromkeys(Candidates.polls, 0)
        for candidate1 in candidate_dictionary.keys():
            candidate_lower = candidate1.lower()
            candidate_dictionary[candidate1] += len(
                [a1 for a1 in video_titles if check_with_accent(candidate_lower, a1.lower())])
        print(candidate_dictionary)
        plt.figure(figsize=(10, 5))
        plot_title_combined = f"{exp}-Candidates From Polls"
        plt.title(plot_title_combined)  # enum to string converion
        values = candidate_dictionary.values()
        plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
        for c, v in candidate_dictionary.items():
            csa_dict[c]['youtube'] = v / sum(values) if sum(values) > 0 else 0
        # [v / sum(values) if sum(values) > 0 else 0 for v in values]
        df = pd.DataFrame.from_dict(csa_dict)
        df.T.plot(kind="bar", stacked=False, figsize=(10, 5))

        plt.xticks(rotation=90)
        plt.tight_layout()
        file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
        plt.savefig("../../plots/csa/transcript_search_" + file_name + ".png")
        # plt.show()
