import glob

import numpy as np

from utils.const import ResultTypes, Experiments
from utils.io import read_json

if __name__ == '__main__':
    # experiment_folder = ["14.01.2022", "07_01_2022"]
    # experiment_folder = ["01_30_2022","01_29_2022","01_28_2022"]

    files = []
    [files.extend(glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/" + f + "/*")) for f in ["03_13_2022"]]
    for t in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK, Experiments.CHANNEL_PERSONALIZATION]:
        experiments_json = []
        [experiments_json.append([a for a in read_json(f) if a['type'] == 'regular']) for f in files if
         (ResultTypes.JSON in f) and (t in f)]
        a = [a for a in experiments_json if a]
        print(t)
        print(np.mean(np.array([len(a) for a in [a for a in experiments_json if a]])))
        # print("Total watched videos during experiments: ", len(experiments_json))
        # url_tag_dict = {d["url"]: d['tags'] for d in experiments_json}
        # print("Total unique urls: ", len(url_tag_dict))
        # url_tag_non_empty_dict = {k: v for k, v in url_tag_dict.items() if len(v) > 0}
        # print("Total non empty tags urls: ", len(url_tag_non_empty_dict))
        #
