import numpy as np

from experiments.utils import check_with_accent
from utils.const import Candidates
from utils.io import read_pickle, read_json


def read(a):
    return {b['url']: {"author": b["author"], "title": b['title']} for b in read_json(a)}


# [{"author": b["author"], "title": b['title']} for b in read_json(a)]
if __name__ == '__main__':
    # f = Parallel(n_jobs=4)(delayed(read)(a) for a in glob.glob("../data/*/*/*.json"))
    #
    # f={k: v for d in f for k, v in d.items()}
    # dump_pickle("title-author.pkl", f)
    f = read_pickle("title-author.pkl")
    f = f.values()
    candidate_dict = dict.fromkeys(Candidates.polls)
    for c in Candidates.polls:
        res = [[check_with_accent(c.lower(), a["author"].lower()), check_with_accent(c.lower(), a["title"].lower())] for
               a in f if
               a['author'] and a['title']]
        res = np.array(res)

        author = np.sum(res[:, 0])
        title = np.sum(res[:, 1])
        authors_name_existed_in_title = np.sum(res[np.where(res[:, 0]), 1])
        title_existed_author = np.sum(res[np.where(res[:, 1]), 0])

        print(c)
        print(
            f'author: {author} title:{title} '
            # f'when candidate name is existed on title, nb videos that it is also the author: {title_existed_author / title:.2f} '
            f'when candidate is the author, nb videos that it\'s name is also existed on title  {authors_name_existed_in_title / author:.2f}')
        # candidate_dict[c] = {"author": np.sum(res[:, 0]), "title": np.sum(res[:, 1])}
