import os.path
import re
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt

from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_experiments, read_experiment_files, read_json, read_multi_folder


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
    plt.bar(candidate_dictionary.keys(), [v / sum(values) for v in values])
    plt.xticks(rotation=90)
    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    plt.savefig("../../plots/walk_based/title_search_from_homepage/" + file_name + ".png")


if __name__ == '__main__':
    experiment_folder = ["14.01.2022", "07_01_2022"]

    for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
        # json_files = read_experiment_files("../07_01_2022", exp, ResultTypes.JSON)
        # csv_files = read_experiment_files("../07_01_2022", exp, ResultTypes.CSV)
        # print("Json files: ", len(json_files))
        # print("Csv files: ", len(csv_files))
        # json_exps = set([os.path.splitext(a)[0] for a in json_files])
        # csv_exps = set([os.path.splitext(a)[0] for a in csv_files])
        #
        # intersection = json_exps.intersection(csv_exps)
        # print("Common experiments: ", len(intersection))
        # experiments_df_list=[]
        # for experiment in intersection:
        #     json_df = pd.read_json(experiment + ResultTypes.JSON)
        #     json_df['url']=json_df.url.str.replace("https://www.youtube.com/watch?v=","",regex=False)
        #     csv_df = pd.read_csv(experiment + ResultTypes.CSV)
        #     exp_df = csv_df.merge(json_df, on="url")
        #     experiments_df_list.append(exp_df)

        experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON)

        # experiments = read_experiments("../../07_01_2022", exp, ResultTypes.JSON)

        # experiments = [x for x in experiments if x]  # remove empty lists
        # video_titles = [f['title'].lower() for e in experiments for f in e if f]

        video_titles = [exp['title'].lower() for e in experiments for exp in e if exp and exp['type'] == 'homepage']

        # Official Candidates
        title_check(Candidates.official, video_titles, exp, "Official Candidates")

        # Polls
        title_check(Candidates.polls, video_titles, exp, "Candidates From Polls")
