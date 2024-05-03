import datetime
import glob
import logging
import os
from collections import defaultdict, Counter

from core.src.config import get_path
from core.src.utils import read_json, dump_json
from gui.src.plots.consts import Candidates, Experiments, ResultTypes, LegislativeParties
from gui.src.utils import check_with_accent, multi_check_with_accent


def title_check(candidates_list, titles, urls):
    candidate_dictionary = defaultdict.fromkeys(candidates_list, 0)
    candidate_url_dictionary = {a: [] for a in candidates_list}
    for candidate, snonyms in candidates_list.items():
        # candidate_lower = candidate.lower()
        videos = [e for a, d in zip(titles, urls) for b, e in zip(a, d) if
                  multi_check_with_accent([candidate] + snonyms, b)]
        candidate_dictionary[candidate] += len(videos)
        candidate_url_dictionary[candidate].extend(videos)
    logging.info(candidate_dictionary)
    values = candidate_dictionary.values()
    return {k: v / sum(values) if sum(values) > 0 else 0 for v in values for k, v in candidate_dictionary.items()}, sum(
        values), candidate_url_dictionary


def generate_plots(experiment_files_path, last_pull_date):
    exp = Experiments.NATIONAL_NEWS_FETCH
    experiments = [a for a in glob.glob(os.path.join(experiment_files_path, "*")) if exp in a and ResultTypes.JSON in a]
    to_date = datetime.datetime.strptime(last_pull_date, "%m_%d_%Y")
    from_date = (datetime.timedelta(hours=-24) + to_date).timestamp()
    to_date = to_date.timestamp()

    related_day_experiments = [a for a in experiments if from_date < int(a.split("-")[-1].split(".")[0]) < to_date]
    # titles = [[b['title'].lower() for b in read_json(a)] for a in related_day_experiments]
    titles = []
    urls = []
    urls_videos_dict = {}
    for a in related_day_experiments:
        title_inner_list = []
        url_inner_list = []
        try:
            for b in read_json(a):
                title_inner_list.append(b['title'].lower())
                url_inner_list.append(b['url'])
                urls_videos_dict[b['url']] = b['title']
        except:
            logging.error("Exception on reading file: " + a)
        finally:
            titles.append(title_inner_list)
            urls.append(url_inner_list)
    total_value = sum(list(map(len, titles)))
    result, political_value, candidate_url_dictionary = title_check(LegislativeParties.Parties, titles, urls)
    most_common_videos = {}
    for a, b in candidate_url_dictionary.items():
        k_top_videos = 5
        if len(b) == 0:
            k_top_videos = 0
        elif 0   < len(b) < k_top_videos:
            k_top_videos = len(b)
        if k_top_videos != 0:
            most_common_videos[a] = [[urls_videos_dict[i], i, j] for i, j in Counter(b).most_common(k_top_videos)]
        else:
            most_common_videos[a] = []

    # most_common_videos = {a: [[urls_videos_dict[i], i, j] for i, j in Counter(b).most_common(5)] if len(b) > 5 else []
    #                       for a, b in candidate_url_dictionary.items()}
    output = get_path(
        f"gui_data/plot_data/legislative_welcome_title_ratio/{last_pull_date}__{int(to_date)}__{int(datetime.datetime.timestamp(datetime.datetime.now()))}.json")
    result = {"candidates": result, "political_mention": political_value, "total_videos": total_value,
              "most_common_videos": most_common_videos}
    dump_json(result, output)
    return result


if __name__ == '__main__':
    os.environ['BASE_DIRECTORY'] = os.path.dirname("/home/ali/Development/bot-crawler/")

    generate_plots("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/05_*", "05_18_2022")
