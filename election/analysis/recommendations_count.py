import glob

from utils.const import Experiments, ResultTypes
from utils.io import read_json

if __name__ == '__main__':

    files = glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/*/*")

    watch_videos = [len([1 for b in read_json(a) if b['type'] == "regular"])
                                 for a
                                 in files if
                                 ResultTypes.JSON in a and (
                                         Experiments.WELCOME_WALK in a or Experiments.NATIONAL_NEWS_WALK in a)]
    print(sum(watch_videos))

    recommendations_from_fetch = [len([1 for b in read_json(a) if b['type'] == "proposal" or b['type'] == "homepage"])
                                  for a
                                  in files if
                                  ResultTypes.JSON in a and (
                                          Experiments.WELCOME_FETCH in a or Experiments.NATIONAL_NEWS_FETCH in a)]
    print(sum(recommendations_from_fetch))

    recommendations_from_walk = [len([1 for b in read_json(a) if b['type'] == "proposal" or b['type'] == "homepage"])
                                 for a
                                 in files if
                                 ResultTypes.JSON in a and (
                                         Experiments.WELCOME_WALK in a or Experiments.NATIONAL_NEWS_WALK in a)]
    print(sum(recommendations_from_walk))
    # for file_type in file_types:
    #     print("%s: %d" % (file_type, len([f for f in files if file_type in f])))
    #
    # for experiment in experiments:
    #     print(experiment)
    #     for file_type in file_types:
    #         print("\t%s: %d" % (file_type, len([f for f in files if (experiment in f) and (file_type in f)])))
    #
    # experiments = [Experiments.WELCOME_WALK,
    #                Experiments.NATIONAL_NEWS_WALK]
