import glob
import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_json, read_multi_folder


def view_check(candidates_list, titles_views, experiment_type, plot_title=""):
    candidate_dictionary = dict.fromkeys(candidates_list)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        views_per_video = [a[1] for a in titles_views if
                           check_with_accent(candidate_lower, a[0])]
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
    if experiment_type == Experiments.WELCOME_FETCH:
        t = "Titles - Fetches from Homepage "
    else:
        t = "Titles - Fetches from National News "
    for k in avg_candidate_dictionary.keys():
        for k_1 in avg_candidate_dictionary[k].keys():
            avg_candidate_dictionary[k][t + k_1] = avg_candidate_dictionary[k].pop(k_1)
    return pd.DataFrame.from_dict(avg_candidate_dictionary)


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


def title_check(candidates_list, titles, experiment_type, plot_title=""):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        candidate_dictionary[candidate] += len(
            [a for a in titles if check_with_accent(candidate_lower, a)])
    print(candidate_dictionary)
    values = candidate_dictionary.values()
    if experiment_type == Experiments.WELCOME_WALK:
        t = "Titles - Walks from Homepage"
    else:
        t = "Titles - Walks from National news"
    candidate_dictionary = {k: {t: v / sum(values) if sum(values) > 0 else 0} for k, v
                            in
                            candidate_dictionary.items()}

    return pd.DataFrame.from_dict(candidate_dictionary)


if __name__ == '__main__':
    # experiment_folder = ["14.01.2022"]
    # dfs_ = []
    # for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
    #     print(exp)
    #     experiments = read_multi_folder("*", exp, ResultTypes.JSON)
    #     video_titles = [clean_view_field(f) for e in experiments for f in e]  # if len(e)>0
    #     print("Total videos: ", len(video_titles))
    #     not_none_video_views = [a for a in video_titles if a and a[1]]
    #     print(
    #         f"Not none views videos: {len(not_none_video_views)} ratio: {len(not_none_video_views) / len(video_titles):.2f}")
    #
    #     df = view_check(Candidates.polls, not_none_video_views, exp, "Candidates From Polls")
    #     dfs_.append(df)
    #
    # for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
    #     print(exp)
    #     files = glob.glob("../../data" + "/*/" + "*" + "/*")
    #     # [files.extend(glob.glob("../../data" + "/*/" + "*" + "/*")) for f in experiment_folder]
    #     experiments_json = []
    #     dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    #
    #     [experiments_json.append([dictfilt(a, ["url", "title", "type"]) for a in read_json(f)]) for f in files if
    #      (ResultTypes.JSON in f) and (exp in f)]  # group each experiment json as one item inside list
    #     experiments = experiments_json
    #
    #     video_titles = [exp['title'].lower() for e in experiments for exp in e if
    #                     exp and exp['type'] == 'proposal' or exp['type'] == 'homepage']
    #
    #     # Polls
    #     dfs_.append(title_check(Candidates.polls, video_titles, exp, "Candidates From Polls"))
    # df = pd.concat(dfs_, axis=0)
    # df.to_csv("data.csv")

    df = pd.read_csv("data.csv")
    df.rename(columns={"Unnamed: 0": "Plots"}, inplace=True)
    df['Plots'] = ["Fetches from Homepage - Avg Video View",
                         "Fetches from Homepage - Avg Occurrence in Title",
                         "Fetches from National News - Avg Video View",
                         "Fetches from National News - Avg Occurrence in Title",
                         "Walks from Homepage - Occurrence in Titles",
                         "Walks from National news - Occurrence in Titles"]
    # df["Experiments"] = df.Experiments.str.replace("Fetches from Homepage Titles", "").str.replace(
    #     "Fetches from National News Titles", "")
    df.set_index("Plots", inplace=True)

    # plt.figure(figsize=(120, 100))

    df.T.plot(kind="bar", stacked=False, figsize=(13, 6))

    plot_title_combined = "Data between 01-24 Jan 22'"  # f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion
    # for candidate,views in candidate_dictionary.items():
    plt.xticks(rotation=90)

    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    # plt.show()
    plt.savefig("../../plots/combined/combined_plot/" + file_name + ".eps")
