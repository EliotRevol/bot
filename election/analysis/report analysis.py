import datetime
import glob
from collections import Counter

from utils.const import Experiments

if __name__ == '__main__':
    files = [datetime.datetime.fromtimestamp(int(a.split("_")[-1].split(".")[0])).strftime("%Y-%m-%d") for a in glob.glob("/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/*/*/*.json")
             if Experiments.NATIONAL_NEWS_WALK in a]
    counter = Counter(files)
    print(sum(counter.values())/len(counter))
