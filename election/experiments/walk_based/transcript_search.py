import glob
import re
from collections import defaultdict

from matplotlib import pyplot as plt

from utils.const import ResultTypes, Experiments, Candidates
from utils.io import read_transcript, read_multi_folder


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

    plt.savefig("../../plots/walk_based/transcript_search/" + file_name + ".png")


if __name__ == '__main__':
    experiment_folder = ["14.01.2022", "07_01_2022"]
    for exp in [Experiments.WELCOME_WALK,
                Experiments.NATIONAL_NEWS_WALK]:

        experiments_json = read_multi_folder(experiment_folder, exp, ResultTypes.TRANSCRIPT)
        url_tag_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}

        video_titles = ["".join(exp['text']).lower() for e in experiments_json for exp in e['transcript']]

        # Official Candidates
        title_check(Candidates.official, video_titles, exp, "Official Candidates")

        # Polls
        title_check(Candidates.polls, video_titles, exp, "Candidates From Polls")
