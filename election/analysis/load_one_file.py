import multiprocessing

from utils.io import read_json

if __name__ == '__main__':
    print(multiprocessing.cpu_count())
    json_file = read_json("../data/widenuc1/01_31_2022/election-channel-personalization_5_1643506172.json")
