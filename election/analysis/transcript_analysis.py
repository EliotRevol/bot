from utils.const import ResultTypes, Experiments
from utils.io import read_multi_folder

if __name__ == '__main__':
    experiment_folder = ["14.01.2022", "07_01_2022"]
    # for exp in [Experiments.WELCOME_WALK,
    #             Experiments.NATIONAL_NEWS_WALK]:
    # print(exp)
    experiments_json = read_multi_folder(experiment_folder, "", ResultTypes.TRANSCRIPT,data_folder="../data")

    print("Total videos with subtitles: ", len(experiments_json))
    url_transcripts_dict = {d["url"]: "".join([a['text'] for a in d['transcript']]) for d in experiments_json}
    print("Total unique urls: ", len(url_transcripts_dict))
