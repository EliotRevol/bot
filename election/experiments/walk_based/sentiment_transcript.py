import multiprocessing
import re
from collections import defaultdict

import numpy as np
import seaborn
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
from tqdm import tqdm
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

from experiments.utils import check_with_accent
from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_multi_folder, dump_pickle, read_pickle


def title_check(candidates_list, titles, experiment_type, plot_title=""):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    for candidate in candidate_dictionary.keys():
        candidate_lower = candidate.lower()
        candidate_dictionary[candidate] += sum(
            [a[1] for a in titles.items() if (candidate_lower in a[0]) or (candidate_lower.replace(" ", "") in a[0])])
    print(candidate_dictionary)
    plt.figure(figsize=(10, 5))

    plot_title_combined = f"{experiment_type}-{plot_title}"
    plt.title(plot_title_combined)  # enum to string converion

    values = candidate_dictionary.values()
    plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])
    plt.xticks(rotation=90)
    plt.tight_layout()
    file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

    plt.savefig("../../plots/walk_based/sentiment_transcript/" + file_name + ".png")


def get_occurred_index_of_candidate(candidate_name, transcript):
    return [i for i in range(len(transcript)) if check_with_accent(candidate_name, transcript[i]['text'].lower())]


def extract_transcripts_of_candidates(url, transcript, candidate_list, analyzer, w=1):
    candidates = []
    score = []
    for candidate_name in candidate_list:
        candidate_name_lower = candidate_name.lower()
        occurrence_ix_list = get_occurred_index_of_candidate(candidate_name_lower, transcript)
        if len(occurrence_ix_list) > 0:
            for ix in occurrence_ix_list:
                matched_text = transcript[ix]['text']
                # if 0 < ix - 1: #TODO open below lines
                #     matched_text = transcript[ix - 1]['text'] + " " + matched_text
                # if ix + 1 < len(transcript):
                #     matched_text = matched_text + " " + transcript[ix + 1]['text']
                score.append(analyzer.polarity_scores(matched_text))
                candidates.append(candidate_name)

    return [url for _ in range(len(candidates))], candidates, score
def extract_transcript_document_of_candidates(url, transcript, candidate_list, analyzer):
    try:
        candidates = []
        score = []
        for candidate_name in candidate_list:
            candidate_name_lower = candidate_name.lower()
            txt=" ".join([a["text"] for a in transcript])
            if check_with_accent(candidate_name_lower,txt.lower()):
            # occurrence_ix_list = get_occurred_index_of_candidate(candidate_name_lower, transcript)
            # if len(occurrence_ix_list) > 0:
            #     for ix in occurrence_ix_list:
            #         matched_text = transcript[ix]['text']
                    # if 0 < ix - 1: #TODO open below lines
                    #     matched_text = transcript[ix - 1]['text'] + " " + matched_text
                    # if ix + 1 < len(transcript):
                    #     matched_text = matched_text + " " + transcript[ix + 1]['text']
                score.append(analyzer.polarity_scores(txt))
                candidates.append(candidate_name)
    except:
        return None


    return [url for _ in range(len(candidates))], candidates, score

if __name__ == '__main__':
    # experiment_folder = ["14.01.2022", "07_01_2022"]
    # experiment_folder = ["01_31_2022"]
    experiment_folder="*"
    # experiment_folder = ["01*", "14.01*"]
    # experiment_folder = ["01_30_2022"]
    w = "infinity"
    generate = False
    if generate:
        for experiment_name in [Experiments.WELCOME_WALK,
                                Experiments.NATIONAL_NEWS_WALK]:
            experiments_transcripts = read_multi_folder(experiment_folder, experiment_name, ResultTypes.TRANSCRIPT,"/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data")
            # experiments_json = read_multi_folder(experiment_folder, exp, ResultTypes.JSON)
            # experiments_json = {b['url']: include_keys(b, ["tags", "author", "title"]) for a in experiments_json for b in a
            #                     if
            #                     b['type'] == 'regular'}

            url_transcripts_dict = {b['url']: b['transcript'] for b in experiments_transcripts}
            analyzer = SentimentIntensityAnalyzer()
            candidate_scores = Parallel(n_jobs=1)(
                delayed(extract_transcript_document_of_candidates)(k, v, Candidates.polls, analyzer) for k, v in
                tqdm(url_transcripts_dict.items()))
            candidate_scores = [a for a in candidate_scores if a and len(a[0]) > 0]  # remove unmatched candidates
            print("flattening scores")
            candidate_scores_flatten = {a[0][0]: [(a[1][b], a[2][b]) for b in range(len(a[0]))] for a in
                                        candidate_scores}
            print("flattened scores")
            # print(candidate_scores)
            result = {"candidate_scores_flatten": candidate_scores_flatten,
                      "experiments_transcripts": experiments_transcripts}

            # candidate_score_dict = defaultdict(list)
            # for e in experiments_transcripts:
            #     if e['url'] in candidate_scores_flatten:
            #         for c, score in candidate_scores_flatten[e['url']]:
            #             candidate_score_dict[c].append((e['url']))
            print("dumping")
            pickle_path = "candidate_sentiment_transcript_RESULT_w_" + str(w) + str(experiment_name) + ".pkl"
            dump_pickle(pickle_path, result)
    plot = True
    unique = False

    if unique:
        prefix = str(w) + "_unique"
    else:
        prefix=str(w)
    if plot:

        for experiment_name in [ Experiments.WELCOME_WALK]:
            pickle_path = "candidate_sentiment_transcript_RESULT_w_" + str(w) + str(experiment_name) + ".pkl"
            print("Reading:", pickle_path)
            result = read_pickle(pickle_path)
            candidate_scores_flatten = result['candidate_scores_flatten']
            experiments_transcripts = result['experiments_transcripts']
            candidate_title_score = defaultdict(list)

            if unique:
                for k,v in candidate_scores_flatten.items():
                    for c, score in v:
                        candidate_title_score[c].append(score)
            else:

                for e in experiments_transcripts:
                    if e['url'] in candidate_scores_flatten:
                        for c, score in candidate_scores_flatten[e['url']]:
                            candidate_title_score[c].append(score)

            canditate_dict = {k: [a['compound'] for a in v] for k, v in candidate_title_score.items()}
            # canditate_dict = defaultdict(list)
            # for a in candidate_title_score:
            #     canditate_dict[a[0]].append(a[3]["compound"])

            plot_name = str(experiment_name).lower().split(".")[1].capitalize()

            plt.figure(figsize=(10, 5))
            seaborn.kdeplot(data=canditate_dict)
            # for a in kde_dict:
            #     plt.hist(kde_dict[a],label=a,bins=1000)

            plt.title("KDE of sentiment analysis of transcripts " + plot_name)
            plt.tight_layout()
            # plt.show()
            plt.savefig("../../plots/walk_based/sentiment_transcript/kde_" + prefix + "_" + plot_name + ".png")

            # plot_title_combined = f"{experiment_type}-{plot_title}"
            # plt.title(plot_title_combined)  # enum to string converion
            plt.figure(figsize=(10, 5))
            plt.title("Avg sentiment analysis of transcripts " + plot_name)
            values = canditate_dict.values()
            plt.bar(canditate_dict.keys(), [np.mean(a) for a in canditate_dict.values()])
            plt.xticks(rotation=90)
            plt.tight_layout()
            # plt.show()
            plt.savefig("../../plots/walk_based/sentiment_transcript/bar_avg_" + prefix + "_" + plot_name + ".png")

            # file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
