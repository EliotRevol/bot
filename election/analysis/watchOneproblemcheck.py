import datetime
import glob

import numpy as np

from experiments.utils import check_with_accent
from utils.const import Experiments, ResultTypes, Candidates
from utils.io import read_json

if __name__ == '__main__':
    files = [a for a in glob.glob("../data" + "/*/02_07_2022/*") if
             Experiments.CHANNEL_PERSONALIZATION in a and ResultTypes.JSON in a]
    files_timestamp = [
        (a.split("_")[-1].replace(".json", ""), [b['author'] for b in read_json(a) if b['type'] == 'regular']) for a in
        files]
    files_timestamp = [a for a in files_timestamp if len(a[1]) > 0]
    # [a.split("_")[-1].replace(".json", "") for a in files]
    candidate_counts = []
    for timestamp, authors in files_timestamp:
        count = 0
        for a in authors:
            if a:
                for c in Candidates.personalized_channels:
                    if check_with_accent(c, a):
                        count += 1
                        break
        candidate_counts.append(count)
    ratios = [(datetime.datetime.fromtimestamp(int(timestamp)).strftime("%d"), count / len(a)) for (timestamp, a), count
              in zip(files_timestamp, candidate_counts)]

    days_ratio = dict()
    for d, v, in ratios:
        if d not in days_ratio:
            days_ratio[d] = []

        days_ratio[d].append(v)
    for d in sorted(days_ratio.keys()):
        print(d, ": ", np.mean(days_ratio[d]))

    print(len(ratios))
    # experiments_json = [] 
    # [experiments_json.append([a for a in read_json(f)]) for f in files if
    #  (ResultTypes.JSON in f) and (experiment_name in f)]  # group each experiment json as one item inside list
    # experiments = experiments_json
    # print(len(experiments))
