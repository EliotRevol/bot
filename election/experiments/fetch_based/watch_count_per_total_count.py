import glob
import re

import pandas as pd
import tqdm
from matplotlib import pyplot as plt

from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_multi_folder, read_json


def title_check(candidates_list, titles_views, experiment_type, plot_title=""):
    candidate_dictionary = dict.fromkeys(candidates_list)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        views_per_video = [a[1] for a in titles_views if
                           (candidate_lower in a[0]) or (candidate_lower.replace(" ", "") in a[0])]
        candidate_dictionary[candidate] = {}
        if len(views_per_video) > 0:
            candidate_dictionary[candidate]['mean'] = sum(views_per_video) / len(views_per_video)
            candidate_dictionary[candidate]['len'] = len(views_per_video)
        else:
            candidate_dictionary[candidate]['mean'] = 0
            candidate_dictionary[candidate]['len'] = 0
    avg_candidate_dictionary = dict.fromkeys(candidates_list)

    for candidate in candidate_dictionary.keys():
        avg_candidate_dictionary[candidate] = {}
        if candidate_dictionary[candidate]['mean'] > 0:
            avg_candidate_dictionary[candidate]['Avg Video View'] = candidate_dictionary[candidate]['mean'] / sum(
                [a['mean'] for a in candidate_dictionary.values()])

            avg_candidate_dictionary[candidate]['Avg Occurrence in Title'] = candidate_dictionary[candidate][
                                                                                 'len'] / sum(
                [a['len'] for a in candidate_dictionary.values()])
        else:
            avg_candidate_dictionary[candidate]['Avg Video View'] = 0
            avg_candidate_dictionary[candidate]['Avg Occurrence in Title'] = 0
    df = pd.DataFrame.from_dict(avg_candidate_dictionary)
    plt.figure(figsize=(10, 5))

    df.T.plot(kind="bar", stacked=False, figsize=(10, 5))
    # print(candidate_dictionary)
    # plt.figure(figsize=(10, 5))

    plot_title_combined = f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion
    # for candidate,views in candidate_dictionary.items():
    # plt.bar(candidate_dictionary.keys(),[v['mean'] / sum([a['mean'] for a in candidate_dictionary.values()]) for v in candidate_dictionary.values()],label="mean",color="r")
    # plt.bar(candidate_dictionary.keys(), [v['len'] / sum([a['len'] for a in candidate_dictionary.values()]) for v in candidate_dictionary.values()],label="count",color="b")
    plt.xticks(rotation=90)

    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    # plt.show()
    plt.savefig("../../plots/fetch_based/watch_count_per_total_count/" + file_name + ".png")


def clean_view_field(exp):
    try:
        return exp['title'].lower(), eval(
            re.sub(r'\W+', '', exp['views']).replace("spectateurs", "").replace("de", "").replace("vues", "").replace(
                "k", "*10**3").replace("K", "*10**3").replace("Md", "*10**6").replace("B", "*10**9").replace("M",
                                                                                                             "*10**6").replace(
                "views", "").replace("watching", ""))
    except:
        # print(exp['views'])
        return None


if __name__ == '__main__':
    experiment_folder = ["*"]

    for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
        path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

        # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

        files = []
        [files.extend(glob.glob(path + "/*/" + f1 + "/*")) for f1 in "*"]
        # experiments_json = []

        experiments_json = [[clean_view_field(a1) for a1 in read_json(f1)] for f1 in tqdm.tqdm(files) if
                            (ResultTypes.JSON in f1) and (exp in f1)]
        experiments = experiments_json
        video_titles = [f for e in experiments for f in e if
                        f]
        print("Total videos: ", len(video_titles))
        not_none_video_views = [a for a in video_titles if a and a[1]]
        print(
            f"Not none views videos: {len(not_none_video_views)} ratio: {len(not_none_video_views) / len(video_titles):.2f}")
        # Official Candidates
        title_check(Candidates.official, not_none_video_views, exp, "Official Candidates")

        # Polls
        title_check(Candidates.polls, not_none_video_views, exp, "Candidates From Polls")
