import re
from collections import defaultdict, OrderedDict

import numpy as np
import tqdm
from matplotlib import pyplot as plt
from scipy.spatial import distance

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_multi_folder, dump_pickle, read_pickle


def title_check(candidates_list, titles, experiment_type, plot_title=""):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        candidate_dictionary[candidate] += len(
            [a for a in titles if (candidate_lower in a) or (candidate_lower.replace(" ", "") in a)])
    print(candidate_dictionary)
    plt.figure(figsize=(10, 5))

    plot_title_combined = f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion

    values = candidate_dictionary.values()
    plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
    plt.xticks(rotation=90)
    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
    plt.savefig("../../plots/walk_based/title_search_from_proposals/" + file_name + ".png")


def cosine_distance(a, welcome_vector):
    a = np.array(a).astype(int)
    b = np.expand_dims(np.array(welcome_vector).astype(int), 0).repeat(len(a), 0)
    return [1 - distance.cosine(x, y) for x, y in zip(a, b)]


def get_vector(welcome_videos, all_videos):
    return [a in welcome_videos for a in all_videos]


if __name__ == '__main__':
    experiment_folder = ["01_25_2022"]
    experiment_name = Experiments.CHANNEL_PERSONALIZATION
    experiments = read_multi_folder('*', experiment_name, ResultTypes.JSON)

    candidate_dictionary = {a.lower(): [] for a in Candidates.personalized_channels}
    all_videos = set()
    # welcome_videos = set()
    for exp in experiments:
        lines = [a for a in exp if a and a['type'] == 'regular']
        if lines and lines[0]['author']:
            found_candidate = None
            for c in candidate_dictionary.keys():
                if check_with_accent(c, lines[0]['author'].lower()):
                    found_candidate = c
                    break
            if found_candidate:
                videos = [a for a in exp if a['type'] == "homepage" or a['type'] == 'regular']
                candidate_dictionary[found_candidate].append(videos)
                all_videos.update(set([a['url'] for a in videos if a['url'] and a['url'] != ""]))
                # welcome_videos.update(set([a['url'] for a in videos if a['videoViewsNB'] == 0 and (
                #         a['url'] and a['url'] != "")]))
    all_videos = OrderedDict.fromkeys(all_videos)
    # welcome_videos = OrderedDict.fromkeys(welcome_videos)
    # welcome_vector = [a in welcome_videos for a in all_videos]

    result = dict.fromkeys(candidate_dictionary.keys())
    for candidate in tqdm.tqdm(candidate_dictionary.keys()):
        recommendations_per_nb_view = [[] for _ in range(6)]
        for e in candidate_dictionary[candidate]:
            if sum([1 for a in e if a['type']=='regular'])==5:
                for i in range(len(recommendations_per_nb_view)):
                    c = [get_vector(a['url'], all_videos) for a in e if a['videoViewsNB'] == i and a['type'] == 'homepage']
                    if len(c) > 0:
                        welcome_videos = set([b['url'] for b in e if b['type'] == 'homepage' and b['videoViewsNB'] == 0])
                        welcome_vector = [a in welcome_videos for a in all_videos]
                        recommendations_per_nb_view[i].append(np.mean(cosine_distance(c, welcome_vector)))
        result[candidate] = recommendations_per_nb_view

    dump_pickle("cosine_dis_same.pkl", result)
    # result = read_pickle("cosine_dis_same.pkl")
    #
    # plt.figure(figsize=(10, 5))
    #
    # # plot_title_combined = f"{experiment_type}-{plot_title}"
    # # plt.title(plot_title_combined)  # enum to string converion
    # for c in result:
    #     plt.plot([np.mean(a) for a in result[c]], label=c)
    # plt.legend()
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.savefig("cosine.png")
