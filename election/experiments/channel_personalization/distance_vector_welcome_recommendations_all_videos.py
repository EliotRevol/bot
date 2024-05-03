import multiprocessing
import re
from collections import defaultdict, OrderedDict

import numpy as np
import seaborn
import tqdm
from fastdist import fastdist
from joblib import delayed, Parallel
from matplotlib import pyplot as plt

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


def cosine_distance(videos, welcome_vector):
    a = np.array(videos).astype(float)
    # b = np.expand_dims(np.array(welcome_vector).astype(float), 0).repeat(len(a), 0)
    # cosine_sim = np.ones_like(a) - fastdist.matrix_to_matrix_distance(a, b, fastdist.cosine, "cosine")
    # fastdist calculates cosine sim instead of cosine dist

    # cosine_sim = fastdist.vector_to_matrix_distance(welcome_vector, a, fastdist.cosine,
    #                                                 "cosine")
    cosine_sim = fastdist.cosine(welcome_vector, a)
    # cosine_sim = np.ones_like(cos_dist) - cos_dist
    # if np.isnan(cosine_sim).any():
    #     raise ArithmeticError
    return cosine_sim
    # return [1 - distance.cosine(x, y) for x, y in zip(a, b)]


def get_vector(welcome_videos, all_videos):
    vector = [a in welcome_videos for a in all_videos.keys()]
    return vector


def run_per_candidate(i, all_videos, welcome_vector, e):
    x = [a['url'] for a in e if a['videoViewsNB'] == i and a['url'] and a['url'] != ""]
    if len(x) > 0:
        c = get_vector(x, all_videos)  # [a in x for a in all_videos.keys()]
        # c = [get_vector(a['url'], all_videos) for a in e if a['videoViewsNB'] == i and a['url'] and a['url'] != ""] # c should be one vector
        # if len(c) > 0:
        cosine_distance_between_welcome_vector = cosine_distance(c, welcome_vector)

        return i, cosine_distance_between_welcome_vector


if __name__ == '__main__':
    generate = False
    if generate:
        experiment_folder = ["*"]
        experiment_name = Experiments.CHANNEL_PERSONALIZATION
        experiments = read_multi_folder("*", experiment_name, ResultTypes.JSON, "/srv/tempdd/ayesilka/srv/tempdd/ayesilka/election_data")
        candidate_dictionary = {a.lower(): [] for a in Candidates.personalized_channels}
        all_videos = set()
        welcome_videos = set()
        for exp in tqdm.tqdm(experiments):
            lines = [a for a in exp if a and a['type'] == 'regular']
            if lines and len(lines) == 5 and None not in [lines[a]['author'] for a in range(5)]:
                found_candidate = None
                for c in candidate_dictionary.keys():

                    if [True] == list(set([check_with_accent(c, lines[i_]['author'].lower()) for i_ in range(5)])):
                        found_candidate = c
                        break
                if found_candidate:
                    videos = [a for a in exp if a['type'] == "homepage"]
                    candidate_dictionary[found_candidate].append(videos)
                    all_videos.update(set([a['url'] for a in videos if a['url'] and a['url'] != ""]))
                    welcome_videos.update(set(
                        [a['url'] for a in videos if a['videoViewsNB'] == 0 and (
                                a['url'] and a['url'] != "")]))
        all_videos = OrderedDict.fromkeys(all_videos)
        welcome_videos = OrderedDict.fromkeys(welcome_videos)
        welcome_vector = [a in welcome_videos for a in all_videos]
        welcome_vector = np.array(welcome_vector).astype(float)

        video_titles = [exp['title'].lower() for e in experiments for exp in e if
                        exp and exp['type'] == 'regular' and exp['title']]
        result = dict.fromkeys(candidate_dictionary.keys())
        for candidate in tqdm.tqdm(candidate_dictionary.keys()):
            recommendations_per_nb_view = [[] for _ in range(6)]

            #
            # for e in candidate_dictionary[candidate]:
            #     for i in range(len(recommendations_per_nb_view)):
            #         c = [get_vector(a['url'], all_videos) for a in e if a['videoViewsNB'] == i]
            #         if len(c) > 0:
            #             cosine_distance_between_welcome_vector = cosine_distance(c, welcome_vector)
            #
            #             recommendations_per_nb_view[i].append(cosine_distance_between_welcome_vector)

            jobs_ = Parallel(n_jobs=multiprocessing.cpu_count())(
                delayed(run_per_candidate)(i, all_videos, welcome_vector, e) for i in
                range(len(recommendations_per_nb_view)) for e in candidate_dictionary[candidate])

            jobs_ = [x for x in jobs_ if x]
            for x in jobs_:
                recommendations_per_nb_view[x[0]].append(x[1])
            result[candidate] = recommendations_per_nb_view

        dump_pickle("cosine_dis_5_all_welcome_1_01__13_02.pkl", result)
    plot = True
    if plot:
        result = read_pickle("cosine_dis_5_all_welcome_1_01__13_02.pkl")
        # for k, v in result.items():
        #     np.mean([np.mean(a) for a in result['macron'][0]])
        #     print(k, ": ", len(v))
        plt.figure(figsize=(10, 5))

        # plot_title_combined = f"{experiment_type}-{plot_title}"
        plt.title("Cosine Sim")  # enum to string converion
        for c in result:
            # plt.plot([np.mean(a) for a in result[c]], label=c)
            plt.plot([np.mean([np.mean(b) for b in a]) for a in result[c]], label=c.capitalize())
        plt.legend()
        # plt.xticks(rotation=90)
        plt.tight_layout()
        # plt.show()
        plt.savefig("../../plots/channel_personalization/cosine_all_welcome_1_01__13_02.png")

        plt.figure(figsize=(10, 5))
        plt.title("KDE Cosine Sim")
        kde_dict = {}  # dict.fromkeys([a for a in range(6)])
        for i in range(0, len(result[next(iter(result.keys()))])):
            for c in result:
                if i not in kde_dict:
                    kde_dict[i] = []
                kde_dict[i].extend(result[c][i])

            # kde_dict[i] = np.concatenate(kde_dict[i])
        seaborn.kdeplot(data=kde_dict)
        # plt.ylim(-0.5e16,None)
        # for a in kde_dict:
        #     plt.hist(kde_dict[a],label=a,bins=1000)
        plt.tight_layout()
        plt.savefig("../../plots/channel_personalization/cosine_all_welcome_kde_allhops_1_01__13_02.png")

        plt.figure(figsize=(10, 5))
        plt.title("KDE Cosine Sim")
        kde_dict.pop(0)
        seaborn.kdeplot(data=kde_dict)
        # plt.ylim(-50,None)

        plt.tight_layout()
        plt.savefig("../../plots/channel_personalization/cosine_all_welcome_kde_no0hop_1_01__13_02.png")
