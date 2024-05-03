import glob

import pandas as pd
import seaborn
import tqdm
from matplotlib import pyplot as plt

from experiments.utils import check_with_accent, include_keys
from utils.const import ResultTypes, Experiments, Candidates, Folders
from utils.io import read_json, dump_pickle, read_pickle


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
        elif check_with_accent(candidate_lower, title_str):
            found_candidates.append(candidate)
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
                for j in range(len(candidates_titles[0])):
                    for k in range(len(candidates_titles[i + 1])):
                        drifts[candidates_titles[0][j]][candidates_titles[i + 1][k]] += 1

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


if __name__ == '__main__':
    experiment_folder = Folders.Round1.minus3month
    # experiment_folder=["*"]
    for experiment_name in [Experiments.NATIONAL_NEWS_WALK, Experiments.WELCOME_WALK]:  #
        # for experiment_name in [Experiments.WELCOME_WALK]:  #
        files = []
        data = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data"
        # data = "/udd/ayesilka/temp_data/ayesilka/election_data/"

        [files.extend(
            glob.glob(data + "/*/" + f + "/*")) for
            f in experiment_folder]
        experiments_json = []

        [experiments_json.append([include_keys(a, ["type", "title", "url", "author", "tags"]) for a in read_json(f)])
         for f in tqdm.tqdm(files) if
         (ResultTypes.JSON in f) and (experiment_name in f)]  # group each experiment json as one item inside list
        experiments = [x for x in experiments_json if x]  # remove empty lists
        video_titles = []
        for exp in tqdm.tqdm(experiments):
            watched_videos = [e for e in exp if e['type'] == 'regular']
            if len(watched_videos) > 1:
                watched_videos = [combine_candidate_clues(a['title'], a['author'], a['tags']) for a in watched_videos]
                # watched_videos = [e['title'].lower() for e in exp if e['type'] == 'regular']
                # if len(watched_videos) > 1 and watched_videos != [""]:  # ignore one or zero hops
                video_titles.append(watched_videos)

        # Official Candidates
        # title_check(Candidates.official, video_titles, exp, "Official Candidates")

        # Polls
        drifts = title_check(Candidates.polls, video_titles, experiment_name, "Candidates From Polls")
        drifts_pkl_ = str(experiment_name) + "_drifts.pkl"
        dump_pickle(drifts_pkl_, drifts)

        pickle = read_pickle(drifts_pkl_)
        pickle[None][None] = 0

        dict_to_plot = {k if k else "Other": {i if i else "Other": j for i, j in v.items() if
                                              i in Candidates.personalized_channels + [None]} for k, v in
                        pickle.items() if k in Candidates.personalized_channels + [None]}
        # for k,v in pickle.items():
        #     for i,j in v.items():
        #         if i not in Candidates.personalized_channels:
        #             del v[i]
        #     if k not in Candidates.personalized_channels:
        #         del pickle[k]

        seaborn.heatmap(pd.DataFrame(dict_to_plot).T, annot=True, fmt="d")
        plt.ylabel("Parent Candidate")
        plt.xlabel("Next Candidate")
        plt.tight_layout()
        # plt.savefig("../../plots/walk_based/title_drift/" + str(experiment_name) + "_drifts.png")
        # plt.savefig("str(experiment_name) + "_drifts.png")
        plt.show()
