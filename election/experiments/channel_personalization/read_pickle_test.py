from utils.io import read_pickle

if __name__ == '__main__':
    pickle = read_pickle("cosine_dis_5_all_welcome.pkl")
    print(len(pickle))
