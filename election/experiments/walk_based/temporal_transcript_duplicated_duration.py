import glob
import re

import pandas as pd
import tqdm
from matplotlib import pyplot as plt

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import dump_pickle, read_pickle, read_transcript

if __name__ == '__main__':
    experiment_folder = [
        "03_11_2022",
        "03_12_2022",
        "03_13_2022",
        "03_14_2022",
        "03_15_2022",
        "03_16_2022",
        "03_17_2022",
        "03_18_2022",
        "03_19_2022",
        "03_20_2022",
        "03_21_2022",
        "03_22_2022",
        "03_23_2022",
        "03_24_2022",
        "03_25_2022",
        "03_26_2022",
        "03_27_2022",
        "03_28_2022",
        "03_29_2022",
        "03_30_2022",
        "03_31_2022",
        "04_01_2022",
        "04_02_2022",
        "04_03_2022",
        "04_04_2022",
        "04_05_2022",
        "04_06_2022",
        "04_07_2022",
        "04_08_2022",
        "04_09_2022",
        "04_10_2022",
        "04_11_2022"
    ]

    # experiment_folder = ["03_24_2022", "03_23_2022"]
    generate = False
    if generate:

        for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
            print(exp)

            path = "/udd/ayesilka/temp_data/ayesilka/election_data/"
            # path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            files = []
            [files.extend(glob.glob(path + "/*/" + f1 + "/*")) for f1 in experiment_folder]
            experiments_json = []

            [experiments_json.extend(
                [(a1, f1.split("/")[-2]) for a1 in read_transcript(f1) if a1['status'] == 'Status.OK']) for f1 in files
                if
                (ResultTypes.TRANSCRIPT in f1) and (exp in f1)]  # each transcript folder represents each experiment

            experiments = experiments_json

            # use this to only access duration , use experiments to for loop over candidates
            video_titles = {"".join(exp['text']).lower(): (exp['duration'], e[1]) for e in experiments for exp in
                            e[0]['transcript']}  # change this to list

            # video_titles = [(f['title'].lower(), f['insertionDate'].split("T")[0]) for e in experiments for f in e if
            #                 f and f['insertionDate'] and f['insertionDate'] != ""]

            # Official Candidates
            candidate_dictionary = {
                c_: {b: {"duration": 0, "count": 0} for b in
                     set([a[1] for a in experiments_json if a[1] and a[1] != ""])} for c_
                in
                Candidates.official}
            for candidate in tqdm.tqdm(candidate_dictionary.keys()):
                candidate_lower = candidate.lower()
                # candidate_dictionary[candidate] += sum(
                #     [1 for text in video_titles if check_with_accent(candidate_lower, text.lower())])
                for text, date in experiments_json:
                    candidate_dictionary_video_count = {a: 0 for a in candidate_dictionary.keys()}
                    for t in text['transcript']:
                        if check_with_accent(candidate_lower, t['text'].lower()):
                            candidate_dictionary[candidate][date]['duration'] += t['duration']
                            # candidate_dictionary[candidate][date]['duration']  = t['duration']
                            candidate_dictionary_video_count[candidate] = 1
                    for cd, vd in candidate_dictionary_video_count.items():
                        if vd > 0:
                            candidate_dictionary[cd][date]['count'] += 1

            dump_pickle("temporal_transcript_duplicated_duration_" + exp.lower() + "_" + ".pkl", candidate_dictionary)
    plot = True
    if plot:
        for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
            print(exp)

            plot_title_combined = f"{exp}"
            print(plot_title_combined)
            file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
            candidate_dictionary = read_pickle("temporal_transcript_duplicated_duration_" + exp.lower() + "_" + ".pkl")
            # plt.figure(figsize=(10, 5))
            fig = plt.figure(figsize=(10, 5))
            plt.title(plot_title_combined)
            for c, v in candidate_dictionary.items():
                date, Scores = zip(*sorted(zip(candidate_dictionary[c].keys(), candidate_dictionary[c].values())))
                # plt.plot(candidate_dictionary[c].keys(),candidate_dictionary[c].values())
                plt.plot(date, [a['duration']/a['count'] if a['count']!=0 else 0 for a in Scores] )

            fig.axes[0].set_xticks(fig.axes[0].get_xticks()[::10])

            # normalized_polls = {a: b / (sum(Polls.round1.values())) for a, b in
            #                     Polls.round1.items()}
            # for c in candidate_dictionary:
            #     candidate_dictionary[c]['Polls'] = normalized_polls[c]
            # values = candidate_dictionary.values()
            # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])

            # df = pd.DataFrame.from_dict(candidate_dictionary)
            # df.T.plot(kind="line", stacked=True, figsize=(10, 5), title=plot_title_combined)
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.savefig(
                "../../plots/walk_based/temporal_transcript_duplicated_duration/temporal_transcript_duplicated_duration_" + file_name + "_" + ".png")

            candidate_dictionary_seconds={a:{b:c['duration'] for b,c in v.items()} for a,v in candidate_dictionary.items()}
            df = pd.DataFrame.from_dict(candidate_dictionary_seconds)
            df.sort_index(inplace=True)
            df.rolling(window=7).mean().plot(title=plot_title_combined, figsize=(15, 7))
            plt.tight_layout()
            plt.savefig(
                "../../plots/walk_based/temporal_transcript_duplicated_duration/temporal_transcript_duplicated_duration__ma7_" + file_name + ".png")
            plt.show()
    print("Finished")
