import glob
import re
from collections import defaultdict

import tqdm
from matplotlib import pyplot as plt

from utils.const import ResultTypes, Experiments, Candidates
from utils.io import dump_pickle, read_json


def title_check(candidates_list, titles_views, experiment_type, plot_title=""):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    for candidate in tqdm.tqdm(candidate_dictionary.keys()):
        candidate_lower = candidate.lower()
        views_per_video = [a[1] for a in titles_views if
                           (candidate_lower in a[0]) or (candidate_lower.replace(" ", "") in a[0])]
        if len(views_per_video) > 0:
            candidate_dictionary[candidate] = sum(views_per_video) / len(views_per_video)

    print(candidate_dictionary)
    plt.figure(figsize=(10, 5))

    plot_title_combined = f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion

    values = candidate_dictionary.values()
    plt.bar(candidate_dictionary.keys(), [v / sum(values) for v in values])
    plt.xticks(rotation=90)
    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    plt.savefig("../../plots/walk_based/watch_count/" + file_name + ".png")

    return candidate_dictionary


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

def clean_view_field(exp):
    try:
        return exp['title'].lower(), eval(
            re.sub(r'\W+', '', exp['views']).replace("spectateurs", "").replace("de", "").replace("vues", "").replace(
                "k", "*10**3").replace("K", "*10**3").replace("Md", "*10**6").replace("B", "*10**9").replace("M",
                                                                                                             "*10**6").replace(
                "views", "").replace("watching", ""))
    except:
        return None


if __name__ == '__main__':
    # experiment_folder = [ "07_01_2022"]
    # experiments = read_experiments("../../07_01_2022", exp, ResultTypes.JSON)
    # experiments = [x for x in experiments if x]  # remove empty lists
    experiment_folder="*"
    # for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
    for exp in [Experiments.NATIONAL_NEWS_WALK]:
        path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
        # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
        # path = "/udd/ayesilka/temp_data/ayesilka/election_data/"

        files = []
        [files.extend(glob.glob(path + "/*/" + f1 + "/*")) for f1 in experiment_folder]
        # experiments_json = []

        experiments_json = [[clean_view_field(a1) for a1 in read_json(f1)] for f1 in tqdm.tqdm(files) if
                            (ResultTypes.JSON in f1) and (exp in f1)]
        experiments = experiments_json
        video_titles = [f for e in experiments for f in e if
                        f]
        print("Total videos: ", len(video_titles))
        not_none_video_views = [a for a in video_titles if a]
        print(
            f"Not none views videos: {len(not_none_video_views)} ratio: {len(not_none_video_views) / len(video_titles):.2f}")
        # Official Candidates
        cand_dict_official = title_check(Candidates.official, not_none_video_views, exp, "Official Candidates")
        dump_pickle("watch_count_official_cand_" + str(exp) + ".pkl", cand_dict_official)

        # Polls
        cand_dict_top5 = title_check(Candidates.personalized_channels, not_none_video_views, exp, "Top5")
        dump_pickle("watch_count_top5_" + str(exp) + ".pkl", cand_dict_top5)
