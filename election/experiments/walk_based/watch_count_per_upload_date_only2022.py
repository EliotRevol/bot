import datetime
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
from scipy.stats import pearsonr

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

        hours_passed = eval(replace)
        if (datetime.datetime.strptime(exp['insertionDate'], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.timedelta(
                hours=hours_passed)).strftime("%Y") == "2022":
            return hours_passed, eval(
                re.sub(r'\W+', '', exp['views']).replace("spectateurs", "").replace("de", "").replace("vues",
                                                                                                      "").replace(
                    "k", "*10**3").replace("K", "*10**3").replace("Md", "*10**6").replace("B", "*10**9").replace("M",
                                                                                                                 "*10**6").replace(
                    "views", "").replace("watching", "")), exp['title'].lower(), exp['author'].lower(), exp['tags'], \
                   exp['type'], exp['insertionDate'], exp['like'], exp['initial_click']

        return None
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


def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3 - q1  # Interquartile range
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out


def assing_first_click(a1):
    first_video = None
    for a in a1:
        if a['type'] == 'regular' and a['title'] and a['author']:
            first_video = find_suitable_candidate(
                [None, None, a['title'].lower(), a['author'].lower(), a['tags']], Candidates.official)[0]
    concat = []
    for a in a1:
        if a:
            a['initial_click'] = first_video
            concat.append(a)
    return concat


if __name__ == '__main__':
    experiment_folder = ["03_03_2022", "03_04_2022", "03_02_2022"]
    generate = False

    if generate:
        for exp in [
            Experiments.WELCOME_WALK,
            Experiments.NATIONAL_NEWS_WALK]:
            path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            # path = "/udd/ayesilka/temp_data/ayesilka/election_data/"
            # experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON, path)
            # video_titles = [clean_view_date_fields(f) for e in experiments for f in e ] # if len(e)>0
            # video_titles = [check_date(f) for e in experiments for f in e]  # if len(e)>0
            # print("Total videos: ", len(video_titles))
            # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"

            files = []
            [files.extend(glob.glob(path + "/*/" + f1 + "/*")) for f1 in experiment_folder]
            # experiments_json = []
            experiments_json = [assing_first_click(read_json(f1)) for f1
                                in tqdm.tqdm(files) if
                                (ResultTypes.JSON in f1) and (exp in f1)]

            experiments_json = [[check_date_view(a1) for a1 in f1 if a1['date'] and a1['date'] != ""] for f1
                                in tqdm.tqdm(experiments_json)]
            # experiments_json = [[check_date_view(a1) for a1 in read_json(f1) if a1['date'] and a1['date'] != ""] for f1
            #                     in tqdm.tqdm(files) if
            #                     (ResultTypes.JSON in f1) and (exp in f1)]
            # need to add first candidate clicked
            clean_dates = [b for a in experiments_json for b in a if b and b[0] and b[1]]  # remove Nons

            dates_per_candiate = Parallel(n_jobs=multiprocessing.cpu_count())(
                delayed(find_suitable_candidate)(a, Candidates.official) for a in tqdm.tqdm(clean_dates))
            # dates_per_candiate=[find_suitable_candidate(a, Candidates.polls) for a in clean_dates]
            pickle_path = "watch_count_date_" + str(exp) + "_2022_sample.pkl"
            dump_pickle(pickle_path, dates_per_candiate)
            print("Dumped " + pickle_path)
    generate_df = True
    if generate_df:
        for exp in [
            Experiments.WELCOME_WALK,
            Experiments.NATIONAL_NEWS_WALK
        ]:
            root_plot_path = "../../plots/walk_based/watch_count_per_upload_date_2022/sample/"
            # root_plot_path="/udd/ayesilka/temp_data/ayesilka/SCRATCH/1747423/" 1760872
            pickle_path = "watch_count_date_" + str(exp) + "_2022_sample.pkl"
            dates_per_candiate = read_pickle(pickle_path)
            print(len(dates_per_candiate))
            data = [[a[0][b], *list(a[1][b])] for a in dates_per_candiate if a[0] for b in
                    range(len(a[0]))]
            frame = pd.DataFrame(data,
                                 columns=['Candidate_Name',  'Hours_After_Upload','Watch_Count', 'Title', 'Author',
                                          'Tag', 'Rec_Type', 'InsertionDate', 'like', 'Initial_Candidate_Clicked'])
            frame.to_csv("watch_count_date_" + str(exp) + "_2022_sample.csv", index=False)
            # pd.DataFrame(data, columns=['Candidate_Name', 'Watch_Count', 'Hours_After_Upload', 'Title', 'Author', 'Tag',
            #                             'Rec_Type', 'InsertionDate'])
            print(len(data))
    plot = False
    if plot:
        for exp in [
            Experiments.WELCOME_WALK,
            Experiments.NATIONAL_NEWS_WALK
        ]:
            root_plot_path = "../../plots/walk_based/watch_count_per_upload_date_2022/sample/"
            # root_plot_path="/udd/ayesilka/temp_data/ayesilka/SCRATCH/1747423/" 1760872
            pickle_path = "watch_count_date_" + str(exp) + "_2022_sample.pkl"
            # pickle_path = "/udd/ayesilka/temp_data/ayesilka/SCRATCH/1747423/watch_count_date_" + str(
            #     exp) + "_2022.pkl"
            for type in ["all"]:  # "proposal", "homepage",
                dates_per_candiate = read_pickle(pickle_path)
                if type != "all":
                    no_cand_videos = [[a[1][0], a[1][1]] for a in dates_per_candiate if
                                      not a[0] and a[1][5] == type]
                    flatten_cand_videos = [[a[0][b], a[1][b]] for a in dates_per_candiate if a[0]
                                           for b in
                                           range(len(a[0])) if a[1][b][5] == type]
                else:
                    no_cand_videos = [[a[1][0], a[1][1]] for a in dates_per_candiate if
                                      not a[0]]
                    flatten_cand_videos = [[a[0][b], a[1][b]] for a in dates_per_candiate if a[0] for b in
                                           range(len(a[0]))]
                candidate_dict = defaultdict(list)
                [candidate_dict[a[0]].append([a[1][0], a[1][1]]) for a in flatten_cand_videos]
                max_hours = max([a[1][1] for a in flatten_cand_videos])
                equal_max_non_cand = [a for a in no_cand_videos if a[1] < max_hours]
                print(len(equal_max_non_cand) / len(no_cand_videos))


                # plt.scatter([a[0] for a in equal_max_non_cand], [a[1] for a in equal_max_non_cand], label="None")
                # for c, v in candidate_dict.items() :
                #     if c in Candidates.personalized_channels:
                #         plt.scatter([a[0] for a in v], [a[1] for a in v], label=c)
                # plt.xticks(rotation=90)
                # plt.legend()
                # plt.tight_layout()
                # plt.show()
                def mean(a):
                    return sum(a) / len(a) if len(a) else 0


                kde_with_video_count_plot = True
                if kde_with_video_count_plot:
                    titles_dict = defaultdict(lambda: {"count": [], "ratio": []})
                    for a in flatten_cand_videos:
                        titles_dict[a[1][2]]['count'].append(a[1][0])
                        titles_dict[a[1][2]]['ratio'].append(a[1][0] / a[1][1] if a[1][1] else 0)

                    mean_count_general = [len(b['ratio']) for a, b in titles_dict.items()]
                    mean_ratio_general = [mean(b['ratio']) for a, b in titles_dict.items()]
                    sum_ratio_general = [sum(b['ratio']) for a, b in titles_dict.items()]
                    print(f"Pearson {exp}\t{pearsonr(mean_count_general, mean_ratio_general)}")
                    print(f"Pearson {exp}\t{pearsonr(mean_count_general, sum_ratio_general)}")
                    candidate_dict_per_date = {a: defaultdict(lambda: defaultdict(list)) for a in candidate_dict}
                    for a in flatten_cand_videos:
                        candidate_name = a[0]
                        date = a[1][6].split("T")[0]
                        title = a[1][2]
                        passed_upload_date = a[1][1]
                        watch_count = a[1][0]
                        candidate_dict_per_date[candidate_name][date][title].append(
                            watch_count / passed_upload_date if passed_upload_date else 0)

                    # video_date_count_dict = {a[1][2] if isinstance(a[1], tuple) else a[1][0][2]: defaultdict(int) for a
                    #                          in dates_per_candiate}
                    # for c in dates_per_candiate:
                    #     v = c[1]
                    #     if isinstance(v, tuple):
                    #         video_date_count_dict[v[2]][v[6].split("T")[0]] += 1
                    #     else:
                    #         video_date_count_dict[v[0][2]][v[0][6].split("T")[0]] += 1

                    candidate_counts_vs_ratios = {a: defaultdict(lambda: {"count": [], "ratio": []}) for a in
                                                  candidate_dict_per_date}
                    counts_vs_ratios = defaultdict(lambda: {"count": [], "ratio": []})
                    counts = []
                    ratio = []
                    for a, b in candidate_dict_per_date.items():
                        for c, d in b.items():
                            for e in d.values():
                                counts_vs_ratios[c]["count"].append(mean(e))
                                counts_vs_ratios[c]["ratio"].append(len(e))
                                candidate_counts_vs_ratios[a][c]["count"].append(mean(e))
                                candidate_counts_vs_ratios[a][c]["ratio"].append(len(e))
                    mean_counts_vs_ratios = {}
                    for a, b in counts_vs_ratios.items():
                        mean_counts_vs_ratios[a] = {"count": mean(b['count']), "ratio": mean(b['ratio'])}

                    mean_candidate_counts_vs_ratios = {a: defaultdict(None) for a in candidate_counts_vs_ratios}
                    for a, b in candidate_counts_vs_ratios.items():
                        for c, d in b.items():
                            mean_candidate_counts_vs_ratios[a][c] = {"count": mean(d['count']),
                                                                     "ratio": mean(d['ratio'])}

                    print(f"Correlation {exp} {type}")
                    print(f"All:\t{pd.DataFrame(mean_counts_vs_ratios).T.corr().iloc[0][1]:.2f}")

                    for c, v in sorted(
                            zip(mean_candidate_counts_vs_ratios.keys(), mean_candidate_counts_vs_ratios.values())):
                        print(f"{c}\t{pd.DataFrame(v).T.corr().iloc[0][1]:.2f}")
                box_plot = False
                if box_plot:
                    plt.figure(figsize=(10, 5))

                    plt.title(str(exp))

                    # division
                    division_dict = dict()
                    for c, v in candidate_dict.items():
                        if c in Candidates.personalized_channels:
                            division_dict[c] = np.array([a[0] / a[1] if a[1] != 0 else 0 for a in v])
                    seaborn.boxplot(data=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in division_dict.items()])),
                                    showfliers=False)
                    plt.xticks(rotation=90)
                    plt.xlabel("Candidates")
                    plt.ylabel("Watch Count / Hours after upload")

                    plt.tight_layout()
                    plt.savefig(
                        root_plot_path + "box_plot_ratio_candidate_top5_" + type + str(
                            exp).lower() + "_only2022.png")
                    plt.clf()

                    plt.figure(figsize=(10, 5))
                    plt.title(str(exp))
                    division_dict['No Candidate'] = np.array(
                        [a[0] / a[1] if a[1] != 0 else 0 for a in equal_max_non_cand])
                    seaborn.boxplot(data=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in division_dict.items()])),
                                    showfliers=False)
                    plt.xticks(rotation=90)
                    plt.xlabel("Candidates")
                    plt.ylabel("Watch Count / Hours after upload")
                    plt.tight_layout()
                    plt.savefig(
                        root_plot_path + type + str(
                            exp).lower() + "_only2022.png")
                    plt.clf()

                    # seaborn.kdeplot(y=[a[0] for a in equal_max_non_cand], x=[a[1] for a in equal_max_non_cand], label="No Cand")
                kde = False
                if kde:

                    candidate_dict_top5_watch_per_hours = {a: {} for a in Candidates.personalized_channels}
                    for c, v in candidate_dict.items():
                        if c in Candidates.personalized_channels:
                            watch_count = [a[0] for a in v]
                            hours_uploaded = [a[1] for a in v]

                            candidate_dict_top5_watch_per_hours[c]['Watch Count'] = watch_count
                            candidate_dict_top5_watch_per_hours[c]['Hours Uploaded'] = hours_uploaded
                    df = pd.DataFrame.from_dict(candidate_dict_top5_watch_per_hours).T
                    plt.figure(figsize=(10, 5))
                    plt.title(str(exp))
                    df = df.explode(["Watch Count", 'Hours Uploaded']).reset_index()
                    df = df.rename(columns={"index": "Candidates"})
                    df_removed_outliers = remove_outlier(df, 'Hours Uploaded')

                    seaborn.kdeplot(data=df_removed_outliers, x="Hours Uploaded", y='Watch Count', hue="Candidates")
                    plt.tight_layout()
                    plt.savefig(
                        root_plot_path + "kde_plot_removed_outliers_ratio_candidate_top5_" + type + str(
                            exp).lower() + "_only2022.png")
                    # plt.show()
                    plt.clf()

                    plt.figure(figsize=(10, 5))
                    plt.title(str(exp))
                    seaborn.kdeplot(data=df, x="Hours Uploaded", y='Watch Count', hue="Candidates")

                    plt.tight_layout()
                    plt.savefig(
                        root_plot_path + "kde_plot_ratio_candidate_top5_" + type + str(
                            exp).lower() + "_only2022.png")
                    plt.clf()

                    # if exp == Experiments.WELCOME_FETCH:
                    #     plt.xlim(0)
                    #     plt.ylim(0)
                    # else:
                    #     plt.xlim(0)
                    # plt.legend()

                    # plt.show()
                    # not_none_video_views = [a for a in video_titles if a and a[1]]
                    # print(
                    #     f"Not none views videos: {len(not_none_video_views)} ratio: {len(not_none_video_views) / len(video_titles):.2f}")
                    # # Official Candidates
                    # # title_check(Candidates.official, not_none_video_views, exp, "Official Candidates")
                    # #
                    # # # Polls
                    # # title_check(Candidates.polls, not_none_video_views, exp, "Candidates From Polls")
    print("Finished")
