import re

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

    # experiment_folder = ["03_24_2022"]
    generate = False
    if generate:

        for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
            print(exp)
            for month, folders in tqdm.tqdm(Folders.Round1.folders_dict.items()):
                path = "/udd/ayesilka/temp_data/ayesilka/election_data/"
                # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
                experiments = read_multi_folder(folders, exp, ResultTypes.JSON, path)

                # experiments = [x for x in experiments if x]  # remove empty lists
                video_titles = [f['title'].lower() for e in experiments for f in e if f]

                # Official Candidates
                candidate_dictionary = {c_: 0 for c_ in Candidates.official}
                for candidate in tqdm.tqdm(candidate_dictionary.keys()):
                    candidate_lower = candidate.lower()
                    candidate_dictionary[candidate] += sum(
                        [1 for text in video_titles if check_with_accent(candidate_lower, text.lower())])
                official_results_dict = {a: b / (sum(Results.round1.values())) for a, b in Results.round1.items()}
                candidate_dictionary = {a: b / (sum(candidate_dictionary.values())) for a, b in
                                        candidate_dictionary.items()}

                print(candidate_dictionary)

                candidate_dictionary = {a: {"Results": official_results_dict[a], "Youtube": candidate_dictionary[a]} for
                                        a
                                        in
                                        candidate_dictionary.keys()}
                dump_pickle("title_search_" + exp.lower() + "_" + month + ".pkl", candidate_dictionary)
    plot = True
    if plot:
        for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
            print(exp)
            for month, folders in Folders.Round1.folders_dict.items():

                plot_title_combined = f"{exp}-vs-Round1 Results"
                # print(plot_title_combined)
                file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
                candidate_dictionary = read_pickle("title_search_" + exp.lower() + "_" + month + ".pkl")
                # plt.figure(figsize=(10, 5))

                normalized_polls = {a: b / (sum(Polls.round1.values())) for a, b in
                                    Polls.round1.items()}
                for c in candidate_dictionary:
                    candidate_dictionary[c]['Polls'] = normalized_polls[c]
                # values = candidate_dictionary.values()
                # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])

                df = pd.DataFrame.from_dict(candidate_dictionary)
                df.T.plot(kind="bar", stacked=False, figsize=(10, 5), title=plot_title_combined)
                plt.xticks(rotation=90)
                plt.tight_layout()
                plt.savefig(
                    "../../../../plots/election_comparison/round1/fetch_based/title_search_" + file_name + "_" + month + ".png")


                # plt.show()

                def get_sorted_candidates(name):
                    result_with_cand = [(c, candidate_dictionary[c][name]) for c, v in candidate_dictionary.items()]
                    candidate = [a[0] for a in result_with_cand]
                    results = [a[1] for a in result_with_cand]
                    return [x for _, x in sorted(zip(results, candidate))]


                r = get_sorted_candidates("Results")
                yt = get_sorted_candidates("Youtube")

                ranking_kendalltau = kendalltau(r, yt)
                ranking_spearman = spearmanr(r, yt)
                result_score = [candidate_dictionary[c]["Results"] for c, v in candidate_dictionary.items()]
                yt_score = [candidate_dictionary[c]["Youtube"] for c, v in candidate_dictionary.items()]
                yt_vs_results_pearson = pearsonr(result_score, yt_score)
                yt_vs_results_kendalltau = kendalltau(result_score, yt_score)
                yt_vs_results_spearman = spearmanr(result_score, yt_score)
                poll_score = [candidate_dictionary[c]["Polls"] for c, v in candidate_dictionary.items()]
                yt_vs_polls_pearson = pearsonr(poll_score, yt_score)
                yt_vs_polls_kendall = kendalltau(poll_score, yt_score)
                yt_vs_polls_spearman = spearmanr(poll_score, yt_score)
                results_vs_polls_pearson = pearsonr(result_score, poll_score)
                results_vs_polls_kendall = kendalltau(result_score, poll_score)
                results_vs_polls_spearman = spearmanr(result_score, poll_score)
                error_yt = sum([abs(a - b) for a, b in zip(result_score, yt_score)])
                # print("Error of YT Experiments: ", error_yt)
                error_poll = sum([abs(a - b) for a, b in zip(result_score, poll_score)])
                # print("Error of Polls: ", error_poll)

                # print("Ranking metrics - Youtube vs. results")
                #
                # print(ranking_kendalltau)
                #
                # print(ranking_spearman)
                #
                #
                # print("Scores metrics - Youtube vs. results")
                # print("Pearson: ", yt_vs_results_pearson)
                # print(yt_vs_results_kendalltau)
                # print(yt_vs_results_spearman)
                #
                # print("Scores metrics - Youtube vs. Polls")
                # print("Pearson: ", yt_vs_polls_pearson)
                # print(yt_vs_polls_kendall)
                #
                # print(yt_vs_polls_spearman)
                #
                # print("Scores metrics - Results vs. Polls")
                # print("Pearson: ", results_vs_polls_pearson)
                # print(results_vs_polls_kendall)
                #
                # print(results_vs_polls_spearman)

                print(
                    f"{re.sub(r'[^0-9]', '', month)}"
                    # f"\t{ranking_spearman[0]:.2f}\t{ranking_kendalltau[0]:.2f}"
                    f"\t{yt_vs_results_spearman[0]:.2f}\t{yt_vs_results_kendalltau[0]:.2f}\t{yt_vs_results_pearson[0]:.2f}"
                    f"\t{error_yt:.2f}"
                    f"\t{yt_vs_polls_spearman[0]:.2f}\t{yt_vs_polls_kendall[0]:.2f}\t{yt_vs_polls_pearson[0]:.2f}"
                    
                    f"\t{results_vs_polls_spearman[0]:.2f}\t{results_vs_polls_kendall[0]:.2f}\t{results_vs_polls_pearson[0]:.2f}"
                    f"\t{error_poll:.2f}")
    print("Finished")
