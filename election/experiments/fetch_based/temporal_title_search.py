import re

import numpy as np
import pandas as pd
import tqdm
from matplotlib import pyplot as plt
from scipy.stats import kendalltau, spearmanr, pearsonr

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates, Results, Folders, Polls
from utils.io import read_multi_folder, dump_pickle, read_pickle

if __name__ == '__main__':
    experiment_folder = [
        "03_11_2022",
        "03_12_2022",
        "03_13_2022",
        "03_14_2022",
        "03_15_2022",
        "03_16_2022",
        "03_17_2022",
        "03_18_2022",
        "03_19_2022",
        "03_20_2022",
        "03_21_2022",
        "03_22_2022",
        "03_23_2022",
        "03_24_2022",
        "03_25_2022",
        "03_26_2022",
        "03_27_2022",
        "03_28_2022",
        "03_29_2022",
        "03_30_2022",
        "03_31_2022",
        "04_01_2022",
        "04_02_2022",
        "04_03_2022",
        "04_04_2022",
        "04_05_2022",
        "04_06_2022",
        "04_07_2022",
        "04_08_2022",
        "04_09_2022",
        "04_10_2022",
        "04_11_2022"
    ]

    experiment_folder = ["03_24_2022", "03_23_2022"]
    generate = False
    if generate:

        for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
            print(exp)

            # path = "/udd/ayesilka/temp_data/ayesilka/election_data/"
            path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON, path)

            # experiments = [x for x in experiments if x]  # remove empty lists
            video_titles = [(f['title'].lower(), f['insertionDate'].split("T")[0]) for e in experiments for f in e if f]

            # Official Candidates
            candidate_dictionary = {c_: {b: 0 for b in set([a[1] for a in video_titles])} for c_ in
                                    Candidates.official}
            for candidate in tqdm.tqdm(candidate_dictionary.keys()):
                candidate_lower = candidate.lower()
                # candidate_dictionary[candidate] += sum(
                #     [1 for text in video_titles if check_with_accent(candidate_lower, text.lower())])
                for text, date in video_titles:
                    if check_with_accent(candidate_lower, text.lower()):
                        candidate_dictionary[candidate][date] += 1

            dump_pickle("temporal_title_search_" + exp.lower() + "_" + ".pkl", candidate_dictionary)
    plot = True
    if plot:
        for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
            print(exp)

            plot_title_combined = f"{exp}"
            print(plot_title_combined)
            file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
            candidate_dictionary = read_pickle("temporal_title_search_" + exp.lower() + "_" + ".pkl")
            # plt.figure(figsize=(10, 5))
            fig=plt.figure(figsize=(15, 7))
            plt.title(plot_title_combined)
            for c, v in candidate_dictionary.items():
                date, Scores = zip(*sorted(zip(candidate_dictionary[c].keys(), candidate_dictionary[c].values())))
                # plt.plot(candidate_dictionary[c].keys(),candidate_dictionary[c].values())
                plt.plot(date, Scores,label=c.capitalize())


            fig.axes[0].set_xticks(fig.axes[0].get_xticks()[::10])


            # normalized_polls = {a: b / (sum(Polls.round1.values())) for a, b in
            #                     Polls.round1.items()}
            # for c in candidate_dictionary:
            #     candidate_dictionary[c]['Polls'] = normalized_polls[c]
            # values = candidate_dictionary.values()
            # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])

            # df = pd.DataFrame.from_dict(candidate_dictionary)
            # df.T.plot(kind="line", stacked=True, figsize=(10, 5), title=plot_title_combined)
            plt.xticks(rotation=90)
            plt.legend()
            plt.tight_layout()
            plt.savefig(
                "../../plots/fetch_based/temporal_title_search/temporal_title_search_" + file_name + "_" + ".png")

            df = pd.DataFrame.from_dict(candidate_dictionary)
            df.sort_index(inplace=True)
            df.rolling(window=7).mean().plot(title=plot_title_combined, figsize=(15, 7))
            plt.tight_layout()
            plt.savefig("../../plots/fetch_based/temporal_title_search/temporal_title_search_ma7_" + file_name +  ".png")
            plt.show()
            #
            #
            # # plt.show()
            #
            # def get_sorted_candidates(name):
            #     result_with_cand = [(c, candidate_dictionary[c][name]) for c, v in candidate_dictionary.items()]
            #     candidate = [a[0] for a in result_with_cand]
            #     results = [a[1] for a in result_with_cand]
            #     return [x for _, x in sorted(zip(results, candidate))]
            #
            #
            # r = get_sorted_candidates("Results")
            # yt = get_sorted_candidates("Youtube")
            # print("Ranking metrics - Youtube vs. results")
            # print(kendalltau(r, yt))
            # print(spearmanr(r, yt))
            #
            # result_score = [candidate_dictionary[c]["Results"] for c, v in candidate_dictionary.items()]
            # yt_score = [candidate_dictionary[c]["Youtube"] for c, v in candidate_dictionary.items()]
            # print("Scores metrics - Youtube vs. results")
            # print("Pearson: ", pearsonr(result_score,
            #                             yt_score))
            # print(kendalltau(result_score,
            #                  yt_score))
            #
            # print(spearmanr(result_score, yt_score))
            # poll_score = [candidate_dictionary[c]["Polls"] for c, v in candidate_dictionary.items()]
            #
            # print("Scores metrics - Youtube vs. Polls")
            # print("Pearson: ", pearsonr(poll_score,
            #                             yt_score))
            # print(kendalltau(poll_score,
            #                  yt_score))
            #
            # print(spearmanr(poll_score, yt_score))
            #
            # print("Scores metrics - Results vs. Polls")
            # print("Pearson: ", pearsonr(result_score,
            #                             poll_score))
            # print(kendalltau(result_score,
            #                  poll_score))
            #
            # print(spearmanr(result_score, poll_score))

    print("Finished")
