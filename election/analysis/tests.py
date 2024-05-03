import glob

from utils.const import Experiments, ResultTypes

if __name__ == '__main__':

    experiments = [Experiments.WELCOME_WALK, Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH,
                   Experiments.NATIONAL_NEWS_WALK]
    file_types = [ResultTypes.CSV, ResultTypes.JSON, ResultTypes.HTML, ResultTypes.TRANSCRIPT, ResultTypes.VARS]
    experiment_folder = ["*"]
    files = []
    [files.extend(glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/" + f + "/*")) for f in experiment_folder]

    for file_type in file_types:
        print("%s: %d" % (file_type, len([f for f in files if file_type in f])))

    for experiment in experiments:
        print(experiment)
        for file_type in file_types:
            print("\t%s: %d" % (file_type, len([f for f in files if (experiment in f) and (file_type in f)])))
