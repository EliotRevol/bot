import glob
from collections import Counter

import tqdm
from statsmodels.iolib import load_pickle

from experiments.utils import check_with_accent
from utils.const import Experiments, ResultTypes, Folders, Candidates
from utils.io import read_json, dump_pickle


def normalize(raw):
    return [i / sum(raw) for i in raw]


channel_dict = {"Macron": "Emmanuel Macron",
                "Zemmour": "Éric Zemmour",
                "Le Pen": "Marine Le Pen",
                "Mélenchon": "JEAN-LUC MÉLENCHON",
                "Pécresse": "Valérie Pécresse"
                }

if __name__ == '__main__':
    path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

    files = []
    month = Folders.Round1.minus3month
    # month = ["04_03*"]
    [files.extend(glob.glob(path + "/*/" + f + "/*")) for f in month]
    generate_watched_videos_set = False
    if generate_watched_videos_set:
        # candidate_dict = {a: [] for a in Candidates.personalized_channels}
        # experiments_json = []
        # for f in tqdm.tqdm(files):
        #     if (ResultTypes.JSON in f) and (Experiments.CHANNEL_PERSONALIZATION in f):
        #         for a in read_json(f):
        #             if a['type'] == 'regular' and a['url'] and a['url'] != "" and a['author'] and a[
        #                 'author'] != "":
        #                 for c in candidate_dict:
        #                     if check_with_accent(c.lower(), a['author'].lower()):
        #                         candidate_dict[c].append(a['url'])
        #
        # candidate_dict_counter = {a: Counter(b) for a, b in candidate_dict.items()}
        candidate_dict = {}
        for a in glob.glob("channels/*.json"):
            print(a)
            candidate_dict[a.split("/")[-1].replace(".json", "")] = [b['url'] for b in read_json(a)]

        dump_pickle("watched_videos.pkl", candidate_dict)
    generate_recommendations_set = False
    if generate_recommendations_set:
        for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]: #Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK
            candidate_dict = {a: [] for a in Candidates.personalized_channels}
            experiments_json = []
            for f in tqdm.tqdm(files):
                if (ResultTypes.JSON in f) and (exp in f):
                    for a in read_json(f):
                        if a['type'] != 'regular' and a['url'] and a['url'] != "" and a['author'] and a[
                            'author'] != "":
                            for c in candidate_dict:
                                # if check_with_accent(c.lower(), a['author'].lower()):
                                if channel_dict[c] == a['author']:
                                    candidate_dict[c].append(a['url'])

            candidate_dict_counter = {a: Counter(b) for a, b in candidate_dict.items()}
            dump_pickle(f"recommendations_{exp}.pkl", candidate_dict_counter)
    calculate_set_difference_values = True
    if calculate_set_difference_values:
        watched_videos = load_pickle("watched_videos.pkl")
        # for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
        #     print(exp)
        #     candidate_dict_counter = load_pickle(f"recommendations_{exp}.pkl")
        #     print(
        #         f"\tWatched Videos\tRecommended Videos\t(Watched-Recommended)/Watched\tWasserstein Over Intersected Videos Counts")
        #
        #     for c in candidate_dict_counter:
        #         watched_videos_set = set(watched_videos[c].keys())
        #         recommended_videos_set = set(candidate_dict_counter[c].keys())
        #
        #         intersection_videos = OrderedDict.fromkeys(watched_videos_set.intersection(recommended_videos_set))
        #         watched_videos_count = [watched_videos[c][a] for a in intersection_videos]
        #         recommended_videos_count = [candidate_dict_counter[c][a] for a in intersection_videos]
        #
        #         distance_count = wasserstein_distance(normalize(watched_videos_count),
        #                                               normalize(recommended_videos_count))
        #         print(
        #             f"{c}\t{len(watched_videos_set)}\t{len(recommended_videos_set)}\t{len(watched_videos_set.difference(recommended_videos_set)) / len(watched_videos_set):.2f}\t{distance_count:.2f}")

        for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK,Experiments.WELCOME_FETCH,Experiments.NATIONAL_NEWS_FETCH]:

            candidate_dict_counter = load_pickle(f"recommendations_{exp}.pkl")
            pretty_exp=exp.replace("election-","").capitalize()
            print(
                f"{pretty_exp}\tChannel Videos\tRec. Videos\tRec./Channel Videos\tTotal Nb. of Rec./Channel Videos")

            for c in candidate_dict_counter:
                watched_videos_set = set(watched_videos[c])
                recommended_videos_set = set(candidate_dict_counter[c].keys())

                recommended_videos_set = recommended_videos_set.difference(
                    recommended_videos_set.difference(watched_videos_set))
                print(
                    f"{c}\t{len(watched_videos_set)}\t{len(recommended_videos_set)}"
                    f"\t{len(recommended_videos_set) / len(watched_videos_set):.2f}\t{sum(candidate_dict_counter[c].values()) / len(watched_videos_set):.2f}")

