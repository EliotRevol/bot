import glob
import multiprocessing
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import seaborn
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
from tqdm import tqdm
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_json, dump_pickle, read_pickle, read_multi_folder


def find_candidate(title, candidate_list):
    author_str, title_str, tags_str = title
    found_candidates = []
    for candidate in candidate_list:
        candidate_lower = candidate.lower()
        if check_with_accent(candidate_lower, author_str):
            found_candidates.append(candidate)
            break  # definitive candidate, only one candidate -> author
        elif check_with_accent(candidate_lower, tags_str):
            found_candidates.append(candidate)
        else:
            check_with_accent(candidate_lower, title_str)
    if len(found_candidates) == 0:
        return [None]
    else:
        return found_candidates


def title_check(candidates_list, titles, experiment_type, plot_title=""):
    # candidate_dictionary = {a:[] for a in candidates_list}
    drifts_to = {a: 0 for a in candidates_list + [None]}
    drifts = {a: drifts_to.copy() for a in candidates_list + [None]}
    walks = []
    for experiment in titles:

        candidates_titles = [find_candidate(hop, candidates_list) for hop in experiment]
        if candidates_titles != [[None]] * len(experiment):
            for i in range(len(candidates_titles) - 1):
                for j in range(len(candidates_titles[i])):
                    for k in range(len(candidates_titles[i + 1])):
                        drifts[candidates_titles[i][j]][candidates_titles[i + 1][k]] += 1

            # candidate_dictionary[candidates_titles[0]].append(candidates_titles[1:])
            # walks.append(candidates_titles)
            # assign first element as key to dictionary (source candidate)
            # values are drifted candidates

    print(drifts)
    return drifts
    # plt.figure(figsize=(10, 5))
    #
    # plot_title_combined = f"{experiment_type}-{plot_title}"
    # plt.title(plot_title_combined)  # enum to string converion
    #
    # values = candidate_dictionary.values()
    # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
    # print(os.path.abspath(os.path.curdir))
    # plt.savefig("../../plots/walk_based/title_drift/" + file_name + ".png")





def combine_candidate_clues(title, author, tags):
    title_str = ""
    author_str = ""
    tags_str = ""

    if len(tags) > 0:
        tags_str = "".join(tags).lower()
    if title:
        title_str = title.lower()
    if author:
        author_str = author.lower()
    return author_str, title_str, tags_str


def find_suitable_candidate(exp, candidate_list):
    author_str, title_str, tags_str = exp['author'].lower(), exp['title'], "".join(exp['tags']).lower()
    found_candidates = []

    for candidate in candidate_list:
        candidate_lower = candidate.lower()
        if check_with_accent(candidate_lower, author_str):
            found_candidates.append(candidate)
            break  # definitive candidate, only one candidate -> author
        elif check_with_accent(candidate_lower, tags_str):
            found_candidates.append(candidate)
        elif check_with_accent(candidate_lower, title_str.lower()):
            found_candidates.append(candidate)
    if len(found_candidates) == 0:
        return None
    else:
        return found_candidates, [title_str for _ in range(len(found_candidates))], [exp['url'] for _ in
                                                                                     range(len(found_candidates))]


def analyze_sentiment(url, title, analyzer):
    score = analyzer.polarity_scores(title)
    return url, score


if __name__ == '__main__':
    # DATA_FOLDER="/srv/tempdd/ayesilka/data"
    # date = "01_27_2022"

    # date="*"
    # DATA_FOLDER = "../../data"
    # for experiment_name in [Experiments.WELCOME_FETCH,Experiments.NATIONAL_NEWS_FETCH]:  #
    #     # files = []
    #
    #     files = glob.glob(DATA_FOLDER + "/*/" + date + "/*")
    #     experiments_json = []
    #
    #     [experiments_json.append([include_keys(a, ["title", "url", "author", "tags"]) for a in read_json(f)])
    #      for f in files if
    #      (ResultTypes.JSON in f) and (experiment_name in f)]  # group each experiment json as one item inside list
    #     experiments = [y for x in experiments_json for y in x if
    #                    x and y['title'] and y['title'] != ""]  # remove empty lists
    #
    #     # experiment_per_candidate = [find_suitable_candidate(a, Candidates.polls) for a in experiments]
    #     print("Starting finding suitable candidate per title")
    #     experiment_per_candidate = Parallel(n_jobs=multiprocessing.cpu_count())(
    #         delayed(find_suitable_candidate)(a, Candidates.polls) for a in tqdm(experiments))
    #     experiment_per_candidate = [a for a in experiment_per_candidate if a]  # eliminate nones
    #     print("Finished finding suitable candidate per title")
    #
    #     experiment_per_candidate_flatten = [(candidate, title, url) for a in experiment_per_candidate for
    #                                         candidate, title, url in
    #                                         zip(*a)]  # flatten duplicate suitable videos
    #     urls_titles = {a[2]: a[1] for a in experiment_per_candidate_flatten}
    #
    #     analyzer = SentimentIntensityAnalyzer()
    #     print("Starting sentiment analysis")
    #     candidate_scores = Parallel(n_jobs=multiprocessing.cpu_count())(
    #         delayed(analyze_sentiment)(k, v, analyzer) for k, v in tqdm(urls_titles.items()))
    #     print("Finished sentiment analysis")
    #     candidate_scores = {a[0]: a[1] for a in candidate_scores}
    #     candidate_title_score = [(*a, candidate_scores[a[2]]) for a in experiment_per_candidate_flatten]
    #     pickle_path = "candidate_title_score_sentiment_" + str(experiment_name) + ".pkl"
    #     dump_pickle(pickle_path, candidate_title_score)
    #     print("Dumped: ", pickle_path)

    for experiment_name in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
        pickle_path = "candidate_title_score_sentiment_" + str(experiment_name) + ".pkl"
        candidate_title_score = read_pickle(pickle_path)
        canditate_dict = defaultdict(list)
        for a in candidate_title_score:
            canditate_dict[a[0]].append(a[3]["compound"])

        plot_name = str(experiment_name).lower().split(".")[1].capitalize()

        plt.figure(figsize=(10, 5))
        seaborn.kdeplot(data=canditate_dict)
        # for a in kde_dict:
        #     plt.hist(kde_dict[a],label=a,bins=1000)


        plt.title("KDE of sentiment analysis of titles " + plot_name)
        plt.tight_layout()
        # plt.show()
        plt.savefig("../../plots/fetch_based/title_sentiment/kde_" + plot_name + ".png")

        # plot_title_combined = f"{experiment_type}-{plot_title}"
        # plt.title(plot_title_combined)  # enum to string converion
        plt.figure(figsize=(10, 5))
        plt.title("Avg sentiment analysis of titles " + plot_name)
        values = canditate_dict.values()
        plt.bar(canditate_dict.keys(),[np.mean(a) for a in canditate_dict.values()])
        plt.xticks(rotation=90)
        plt.tight_layout()
        # plt.show()
        plt.savefig("../../plots/fetch_based/title_sentiment/bar_avg_" + plot_name + ".png")

        # file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
