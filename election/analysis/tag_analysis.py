import glob

from utils.const import ResultTypes
from utils.io import read_json

if __name__ == '__main__':
    experiment_folder = ["14.01.2022", "07_01_2022"]
    files = []
    [files.extend(glob.glob("../data/*/" + f + "/*")) for f in experiment_folder]

    experiments_json = []
    [experiments_json.extend([a for a in read_json(f) if a['type'] == 'regular']) for f in files if
     ResultTypes.JSON in f]
    print("Total watched videos during experiments: ", len(experiments_json))
    url_tag_dict = {d["url"]: d['tags'] for d in experiments_json}
    print("Total unique urls: ", len(url_tag_dict))
    url_tag_non_empty_dict = {k: v for k, v in url_tag_dict.items() if len(v) > 0}
    print("Total non empty tags urls: ", len(url_tag_non_empty_dict))
