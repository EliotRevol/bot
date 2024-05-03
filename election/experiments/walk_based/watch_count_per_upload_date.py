import glob
import multiprocessing
import re
from collections import defaultdict

import numpy as np
import pandas as pd
import seaborn
import tqdm
from joblib import Parallel, delayed
from matplotlib import pyplot as plt

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import dump_pickle, read_pickle, read_json


def clean_view_date_fields(exp):
    try:
        return exp['title'].lower(), eval(
            re.sub(r'\W+', '', exp['views']).replace("spectateurs", "").replace("de", "").replace("vues", "").replace(
                "k", "*10**3").replace("K", "*10**3").replace("Md", "*10**6").replace("B", "*10**9").replace("M",
                                                                                                             "*10**6").replace(
                "views", "").replace("watching", ""))
    except:
        # print(exp['views'])
        return None


def check_date_view(exp):
    try:
        if True in [a in exp['date'].lower() for a in
                    ["now", "scheduled", "première", "live", "planifié", "premieres"]]:
            replace = "0"
        else:
            replace = exp['date'].strip().replace("il y a ", "").replace("Diffusé", "").replace("mois",
                                                                                                "*24*30").replace(
                "jour",
                "*24").replace(
                "jours", "*24").replace("heure", "*1").replace("ACTUELLEMENT EN DIRECT", "*0").replace("semaine",
                                                                                                       "*7*24").replace(
                "an",
                "*24*365").replace("EN DIRECT", "0").replace(" ago", "").replace("Streamed", "").replace("week",
                                                                                                         "*7*24").replace(
                "day", "*24").replace("hour",
                                      "*1").replace("year",
                                                    "*24*365").replace(
                "month", "*4*30").replace(
                "s", "")

            if True in [a in replace.lower() for a in ["minute", "*0"]]:
                replace = "0"
        return eval(replace), eval(
            re.sub(r'\W+', '', exp['views']).replace("spectateurs", "").replace("de", "").replace("vues", "").replace(
                "k", "*10**3").replace("K", "*10**3").replace("Md", "*10**6").replace("B", "*10**9").replace("M",
                                                                                                             "*10**6").replace(
                "views", "").replace("watching", "")), exp['title'].lower(), exp['author'].lower(), exp['tags']
    except Exception as e:
        pass


def find_suitable_candidate(exp, candidate_list):
    author_str, title_str, tags_str = exp[3].lower(), exp[2], "".join(exp[4]).lower()
    found_candidates = []

    for candidate in candidate_list:
        candidate_lower = candidate.lower()
        if check_with_accent(candidate_lower, author_str):
            found_candidates.append(candidate)
            break  # definitive candidate, only one canParallel(n_jobs=multiprocessing.cpu_count())(

        elif check_with_accent(candidate_lower, tags_str):
            found_candidates.append(candidate)
        elif check_with_accent(candidate_lower, title_str.lower()):
            found_candidates.append(candidate)
    if len(found_candidates) == 0:
        return None, exp
    else:
        return found_candidates, [exp for _ in
                                  range(len(found_candidates))]


if __name__ == '__main__':
    experiment_folder = ["03_03_2022"]
    generate = True

    # TODO FILTER THIS CODE ONLY FOR 2022
    if generate:
        for exp in [
            Experiments.WELCOME_WALK,
            Experiments.NATIONAL_NEWS_WALK]:
            path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

            # experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON, path)
            # video_titles = [clean_view_date_fields(f) for e in experiments for f in e ] # if len(e)>0
            # video_titles = [check_date(f) for e in experiments for f in e]  # if len(e)>0
            # print("Total videos: ", len(video_titles))
            # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

            files = []
            [files.extend(glob.glob(path + "/*/" + f1 + "/*")) for f1 in experiment_folder]
            # experiments_json = []

            experiments_json = [[check_date_view(a1) for a1 in read_json(f1) if a1['date'] and a1['date'] != ""] for f1
                                in tqdm.tqdm(files) if
                                (ResultTypes.JSON in f1) and (exp in f1)]

            clean_dates = [b for a in experiments_json for b in a if b and b[0] and b[1]]  # remove Nons

            dates_per_candiate = Parallel(n_jobs=multiprocessing.cpu_count())(
                delayed(find_suitable_candidate)(a, Candidates.official) for a in tqdm.tqdm(clean_dates))
            # dates_per_candiate=[find_suitable_candidate(a, Candidates.polls) for a in clean_dates]
            pickle_path = "watch_count_date_" + str(exp) + ".pkl"
            dump_pickle(pickle_path, dates_per_candiate)
            print("Dumped " + pickle_path)
    plot = True
    if plot:
        for exp in [
            Experiments.WELCOME_WALK,
            Experiments.NATIONAL_NEWS_WALK
        ]:
            pickle_path = "watch_count_date_" + str(exp) + ".pkl"
            dates_per_candiate = read_pickle(pickle_path)
            no_cand_videos = [[a[1][0], a[1][1]] for a in dates_per_candiate if not a[0]]
            flatten_cand_videos = [[a[0][b], a[1][b]] for a in dates_per_candiate if a[0] for b in range(len(a[0]))]
            candidate_dict = defaultdict(list)
            [candidate_dict[a[0]].append([a[1][0], a[1][1]]) for a in flatten_cand_videos]
            max_hours = max([a[1][1] for a in flatten_cand_videos])
            equal_max_non_cand = [a for a in no_cand_videos if a[1] < max_hours]
            print(len(equal_max_non_cand) / len(no_cand_videos))

            plt.figure(figsize=(10, 5))

            # plt.scatter([a[0] for a in equal_max_non_cand], [a[1] for a in equal_max_non_cand], label="None")
            # for c, v in candidate_dict.items() :
            #     if c in Candidates.personalized_channels:
            #         plt.scatter([a[0] for a in v], [a[1] for a in v], label=c)
            # plt.xticks(rotation=90)
            # plt.legend()
            # plt.tight_layout()
            # plt.show()
            plt.title(str(exp))

            # division
            division_dict = dict()
            for c, v in candidate_dict.items():
                if c in Candidates.personalized_channels:
                    division_dict[c] = np.array([a[0] / a[1] if a[1] != 0 else 0 for a in v])
            seaborn.boxplot(data=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in division_dict.items()])),
                            showfliers=False)

            # seaborn.kdeplot(y=[a[0] for a in equal_max_non_cand], x=[a[1] for a in equal_max_non_cand], label="No Cand")

            if False:
                for c, v in candidate_dict.items():
                    if c in Candidates.personalized_channels:
                        seaborn.kdeplot(y=[a[0] for a in v if a[1] < 4320], x=[a[1] for a in v if a[1] < 4320], label=c)

            plt.xticks(rotation=90)
            plt.xlabel("Candidates")
            plt.ylabel("Watch Count / Hours after upload")

            # if exp == Experiments.WELCOME_FETCH:
            #     plt.xlim(0)
            #     plt.ylim(0)
            # else:
            #     plt.xlim(0)
            # plt.legend()
            plt.tight_layout()
            plt.savefig(
                "../../plots/walk_based/watch_count_per_upload_date/box_plot_ratio_candidate_polls" + str(
                    exp).lower() + ".png")
            # plt.show()
            # not_none_video_views = [a for a in video_titles if a and a[1]]
            # print(
            #     f"Not none views videos: {len(not_none_video_views)} ratio: {len(not_none_video_views) / len(video_titles):.2f}")
            # # Official Candidates
            # # title_check(Candidates.official, not_none_video_views, exp, "Official Candidates")
            # #
            # # # Polls
            # # title_check(Candidates.polls, not_none_video_views, exp, "Candidates From Polls")

            plt.title(str(exp))
            plt.figure(figsize=(10, 5))
            division_dict['No Candidate'] = np.array([a[0] / a[1] if a[1] != 0 else 0 for a in equal_max_non_cand])
            seaborn.boxplot(data=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in division_dict.items()])),
                            showfliers=False)
            plt.xticks(rotation=90)
            plt.xlabel("Candidates")
            plt.ylabel("Watch Count / Hours after upload")
            plt.tight_layout()
            plt.savefig(
                "../../plots/walk_based/watch_count_per_upload_date/box_plot_ratio_candidate_polls_withwelcome" + str(
                    exp).lower() + ".png")
