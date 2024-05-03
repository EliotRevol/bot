import tqdm

from utils.const import ResultTypes, Experiments
from utils.io import read_multi_folder

if __name__ == '__main__':
    experiment_folder = ["05_1*"]
    path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
    experiments_json = read_multi_folder("*", Experiments.NATIONAL_NEWS_WALK, ResultTypes.TRANSCRIPT, path)
    filtered_transcript = [b['text'] for a in tqdm.tqdm(experiments_json) for b in a['transcript']]
    nupes = [a for a in filtered_transcript if "nupes" in a.lower()]
    print(sum(nupes))
