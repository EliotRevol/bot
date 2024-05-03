import pandas as pd
from matplotlib import pyplot as plt

from utils.io import read_pickle

if __name__ == '__main__':
    # df = pd.read_csv("nsppolss.csv")
    # df = df[df.candidat.str.contains("|".join(Candidates.official))]
    # df = df[df.fin_enquete.str.contains("2022")]
    # df.to_csv("filtered.csv", index=False)
    df = pd.read_csv("filtered.csv")
    df = df[df.tour == 'Premier tour']
    df = df[['candidat', 'intentions', 'fin_enquete']].set_index(["fin_enquete"])
    file = read_pickle(
        "/home/ali/Development/election/experiments/walk_based/temporal_title_search_election-welcome-walk_.pkl")
    # df_dict=pd.DataFrame.from_dict(file)
    df = df.pivot_table(values='intentions', index=df.index, columns='candidat', aggfunc='mean')
    df.plot(figsize=(10, 6))
    plt.tight_layout()
    plt.savefig("polls_2022_premier_tour.png")
    df.rolling(window=7).mean().plot(figsize=(10, 6))
    plt.tight_layout()
    plt.savefig("polls_2022_premier_tour_ma7.png")

    # df.pivot_table(values='intentions', index=df.index, columns='candidat', aggfunc='mean').plot()
