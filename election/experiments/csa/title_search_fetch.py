import glob
import re
from collections import defaultdict

import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

from csa.extract_from_csa_data import get_time
from experiments.utils import check_with_accent, include_keys, combine_candidate_clues, find_candidate
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_multi_folder, read_json


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

    experiment_folder = ["14.01.2022", "01_*",
                         "02_01_2022",
                         "02_02_2022",
                         "02_03_2022",
                         "02_04_2022",
                         "02_05_2022",
                         "02_06_2022",
                         "02_07_2022",
                         "02_08_2022",
                         "02_09_2022",
                         "02_10_2022",
                         "02_11_2022",
                         "02_12_2022",
                         "02_13_2022",
                         "02_14_2022"
                         ]
    # experiment_folder = ["02_14_2022"]
    csa = pd.read_csv("pres_2022.csv")
    csa['total_time'] = csa[["time_candidat", "time_support", "time_mention"]].sum(axis=1)
    csa_dict = {}
    for candidate in Candidates.polls:
        for _, t in csa.groupby("candidat")['total_time'].sum().reset_index().iterrows():
            if check_with_accent(candidate, t['candidat']):
                csa_dict[candidate] = t['total_time']

    csa_df = pd.read_csv("TP-TA_Presidentielle_2022__1er janvier au 13 février 2022.csv", sep=";",
                         encoding="ISO-8859-1", header=None,
                         names=["Channel", "_", "Candidat", "Type", "Duration", "ratio"])

    csa_df = csa_df[csa_df.Type.isin(["Candidat", "Soutiens", "Antenne"])]
    csa_df['Hours'] = csa_df.Duration.apply(lambda x: get_time(x))
    # experiment_folder = ["14.01.2022", "07_01_2022"]
    csa_df = csa_df.groupby("Candidat").sum("Hours").reset_index()
    csa_dict = {}
    for candidate in Candidates.polls:
        cand_df = csa_df[csa_df.Candidat.apply(lambda x: check_with_accent(candidate.lower(), x.lower()))]
        csa_dict[candidate] = cand_df.Hours.iloc[0]

    csa_dict = {k: {"csa": v / sum(csa_dict.values()) if sum(csa_dict.values()) > 0 else 0} for k, v in
                csa_dict.items()}
    for exp in [Experiments.WELCOME_FETCH,
                Experiments.NATIONAL_NEWS_FETCH]:
        # experiments_json = read_multi_folder(experiment_folder, exp, ResultTypes.JSON,
        #                                      "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/")
        # url_tag_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}
        files = []
        [files.extend(
            glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data" + "/*/" + f + "/*")) for
         f in experiment_folder]
        experiments_json = []

        [experiments_json.append([include_keys(a, ["type", "title", "url", "author", "tags"]) for a in read_json(f)])
         for f in tqdm(files) if
         (ResultTypes.JSON in f) and (exp in f)]  # group each experiment json as one item inside list
        experiments = [x for x in experiments_json if x]  # remove empty lists
        video_titles = []
        candidate_dictionary = { a: 0 for a in Candidates.polls}

        for experiment_instance in tqdm(experiments):
            # watched_videos = [e for e in experiment_instance if e['type'] == 'regular']
            watched_videos=experiment_instance
            if len(watched_videos) > 1:
                watched_videos = [combine_candidate_clues(a['title'], a['author'], a['tags']) for a in watched_videos]
                # watched_videos = [e['title'].lower() for e in exp if e['type'] == 'regular']
                # if len(watched_videos) > 1 and watched_videos != [""]:  # ignore one or zero hops
                candidate_matched=[find_candidate(a,csa_dict.keys()) for a in watched_videos ]
                for c in candidate_matched:
                    if c!=[None]:
                        for v in c:
                            candidate_dictionary[v] += 1




        print(candidate_dictionary)
        plt.figure(figsize=(10, 5))
        plot_title_combined = f"{exp}-Candidates From Polls"
        plt.title(plot_title_combined)  # enum to string converion
        values = candidate_dictionary.values()
        plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])

        for c, v in candidate_dictionary.items():
            csa_dict[c]['youtube'] = v / sum(values) if sum(values) > 0 else 0
        df = pd.DataFrame.from_dict(csa_dict)
        df.T.plot(kind="bar", stacked=False, figsize=(10, 5))
        plt.xticks(rotation=90)
        plt.tight_layout()
        file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
        plt.savefig("../../plots/csa/title_search_fetch" + file_name + ".png")