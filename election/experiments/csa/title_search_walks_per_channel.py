import datetime
import glob
import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

from experiments.utils import check_with_accent, combine_candidate_clues, find_candidate, include_keys
from utils.const import ResultTypes, Experiments, Candidates, Channels
from utils.io import read_transcript, read_json_gz, read_json, dump_pickle, read_pickle


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


def get_time(date):
    h, m, s = date.split(":")
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


def check_tv(tv_in_csa, author):
    for tv in tv_in_csa:
        if author and tv.lower().replace(" ", "") == author.lower().replace(" ", ""):
            return True
    return False


def check_tv_one(tv_in_csa, author):
    if tv_in_csa and author:
        return tv_in_csa.lower().replace(" ", "").replace("tv", "") == author.lower().replace(" ", "").replace("tv", "")
    return False


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
    # experiment_folder = ["02_12_2022"
    #                      "02_13_2022",
    #                      "02_14_2022",
    #                      "02_15_2022",
    #                      "02_16_2022",
    #                      "02_17_2022"
    #                      ]

    generation = True
    if generation:
        csa_df = pd.read_csv("TP-TA_Presidentielle_2022__1er janvier au 13 février 2022.csv", sep=";",
                             encoding="ISO-8859-1", header=None,
                             names=["Channel", "_", "Candidat", "Type", "Duration", "ratio"])

        csa_df = csa_df[csa_df.Type.isin(["Candidat", "Soutiens", "Antenne"])]
        csa_df['Hours'] = csa_df.Duration.apply(lambda x: get_time(x))
        # experiment_folder = ["14.01.2022", "07_01_2022"]

        csa_dict = {}
        for candidate in Candidates.polls:
            csa_dict[candidate] = {}
            cand_df = csa_df[csa_df.Candidat.apply(lambda x: check_with_accent(candidate.lower(), x.lower()))]
            for _, t in cand_df.groupby("Channel").sum("Hours").reset_index().iterrows():
                if True in [check_with_accent(t['Channel'].lower(), a.lower()) for a in Channels.tv_in_csa]:
                    csa_dict[candidate][t['Channel']] = {"csa": t['Hours'], "yt": 0}
            # # csa["candidat"]==
            # for _, t in csa.groupby("candidat")['total_time'].sum().reset_index().iterrows():
            #     pass
        # csa_dict = {k: {"csa": v / sum(csa_dict.values()) if sum(csa_dict.values()) > 0 else 0} for k, v in
        #             csa_dict.items()}
        for exp in [Experiments.WELCOME_WALK,
                    Experiments.NATIONAL_NEWS_WALK]:
            files1 = []
            [files1.extend(glob.glob(
                "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/" + "/*/" + f1 + "/*"))
                for f1 in experiment_folder]
            json = [[include_keys(a1,["url","author","title","tags","type"]) for a1 in read_json(f1)] for f1 in tqdm(files1) if
                    (ResultTypes.JSON in f1) and (exp in f1)]  # group each experiment json as one item inside list

            experiments_json = json
            author_json=[{a2['url']: a2['author'] for a2 in f if a2['type'] == 'regular'} for f in
             json
             ]
            # url_tag_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}
            # files = []
            # [files.extend(
            #     glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/" + "/*/" + f + "/*"))
            #     for
            #     f in experiment_folder]
            # # # group each experiment json as one item inside list
            # author_json = [{a2['url']: a2['author'] for a2 in read_json(f) if a2['type'] == 'regular'} for f in
            #                tqdm(files)
            #                if
            #                (ResultTypes.JSON in f) and (exp in f)]
            url_author_dict = {k: v for a in author_json for k, v in a.items() if check_tv(Channels.tv_in_csa, v)}

            # url - text
            video_titles = [(e['url'], combine_candidate_clues(e['title'], e['author'], e['tags'])) for experiment in
                            experiments_json for e in experiment
                            if e['url'] in url_author_dict.keys()]

            # we have author url text and csa
            # candidate_dictionary = defaultdict.fromkeys(Candidates.polls, 0)

            for url, video in video_titles:
                candidate_matched = find_candidate(video, csa_dict.keys())
                if candidate_matched != [None]:
                    author_yt_name = url_author_dict[url]
                    for candidate1 in candidate_matched:
                        for tv in Channels.tv_in_csa:
                            if check_tv_one(tv, author_yt_name):
                                if tv in csa_dict[candidate1]:
                                    csa_dict[candidate1][tv]['yt'] += 1
                                else:
                                    csa_dict[candidate1] = {tv: {"yt": 1, "csa": 0}}
                                break
            tv_dict = {tv: defaultdict() for tv in Channels.tv_in_csa}
            for candidates in csa_dict.keys():
                for tv in csa_dict[candidates].keys():
                    tv_dict[tv][candidates] = csa_dict[candidates][tv]

            # normalize
            normalized_tv_dict = {a: defaultdict() for a in tv_dict.keys()}
            for tv, candidates in tv_dict.items():
                sum_csa = sum([a['csa'] for a in candidates.values()])
                sum_yt = sum([a['yt'] for a in candidates.values()])
                for c, v in candidates.items():
                    if v["csa"] != 0:
                        csa_val = v["csa"] / sum_csa
                    else:
                        csa_val = 0
                    if v["yt"] != 0:
                        yt_val = v["yt"] / sum_yt
                    else:
                        yt_val = 0
                    normalized_tv_dict[tv][c] = {"csa": csa_val, "yt": yt_val}
            dump_pickle("csa_title_per_tv_1_01__13_02" + str(exp) + ".pkl", normalized_tv_dict)

    plot = True
    if plot:
        for exp in [Experiments.WELCOME_WALK,
                    Experiments.NATIONAL_NEWS_WALK]:
            normalized_tv_dict = read_pickle("csa_title_per_tv_1_01__13_02" + str(exp) + ".pkl")
            for channels in normalized_tv_dict.keys():
                # plt.figure(figsize=(10, 5))
                plot_title_combined = f"{exp}-{channels}"

                df = pd.DataFrame.from_dict(normalized_tv_dict[channels])
                fig = df.T.plot(kind="bar", stacked=False, figsize=(10, 5)).get_figure()
                plt.title(plot_title_combined)  # enum to string converion

                plt.xticks(rotation=90)
                plt.tight_layout()
                plt.savefig("../../plots/csa/channels_title/" + str(exp.lower()) + "/" + channels + ".png")
                plt.cla()

            # print(candidate_dictionary)
            # plt.figure(figsize=(10, 5))
            # plot_title_combined = f"{exp}-Candidates From Polls"

            # values = candidate_dictionary.values()
            # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
            # for c, v in candidate_dictionary.items():
            #     csa_dict[c]['youtube'] = v / sum(values) if sum(values) > 0 else 0
            # # [v / sum(values) if sum(values) > 0 else 0 for v in values]
            # df = pd.DataFrame.from_dict(csa_dict)
            # df.T.plot(kind="bar", stacked=False, figsize=(10, 5))
            #
            # plt.xticks(rotation=90)
            # plt.tight_layout()
            # file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
            # plt.savefig("../../plots/csa/transcript_search_" + file_name + ".png")
            # # plt.show()
