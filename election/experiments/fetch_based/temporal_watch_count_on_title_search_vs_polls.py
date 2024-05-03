import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from utils.const import Experiments, Candidates
from utils.io import read_pickle

if __name__ == '__main__':
    for exp in [Experiments.WELCOME_FETCH, Experiments.NATIONAL_NEWS_FETCH]:
        candidate_dictionary = read_pickle("temporal_watch_count_title_search_" + exp.lower() +  ".pkl")
        candidate_dictionary = {a: b for a, b in candidate_dictionary.items() if a in Candidates.personalized_channels}
        df_yt = pd.DataFrame.from_dict(candidate_dictionary)
        df_yt.rename(index={"14.01.2022": "01_14_2022"}, inplace=True)
        # df_yt.set_index(pd.to_datetime(df_yt.index, format="%m_%d_%Y").strftime("%Y-%m-%d"), inplace=True)
        df_yt.sort_index(inplace=True)
        df_yt = df_yt.div(df_yt.sum(axis=1), axis=0) * 100

        df_polls = pd.read_csv("../../polls/filtered.csv")
        df_polls = df_polls[df_polls.tour == 'Premier tour']

        df_polls = df_polls[df_polls.candidat.str.contains("|".join(Candidates.personalized_channels))]
        df_polls = df_polls[['candidat', 'intentions', 'fin_enquete']].set_index(["fin_enquete"])
        df_polls = df_polls.pivot_table(values='intentions', index=df_polls.index, columns='candidat', aggfunc='mean')
        # df_polls.columns = df_polls.columns.str.split(" ")[-1]
        df_polls.rename(columns={'Emmanuel Macron': 'Macron', 'Eric Zemmour': 'Zemmour',
                                 'Jean-Luc Mélenchon': 'Mélenchon',
                                 'Marine Le Pen': 'Le Pen', 'Valérie Pécresse': 'Pécresse'}, inplace=True)
        df_polls = df_polls[~df_polls.index.isin(["2022-04-" + str(a).zfill(2) for a in range(9, 23)])]

        df_polls = df_polls.interpolate()
        df_polls = df_polls.reindex(columns=df_yt.columns)
        df_merged = pd.merge(df_polls, df_yt, left_index=True, right_index=True, how='inner',
                             suffixes=["_Polls", "_YouTube"])
        df_merged = df_merged.rolling(7).mean()
        # df_merged.plot(figsize=(10, 5))

        df_polls_plot = df_merged[[a for a in df_merged.columns if 'Polls' in a]]
        df_yt_plot = df_merged[[a for a in df_merged.columns if 'YouTube' in a]]

        ax = df_polls_plot.plot(figsize=(10, 6))
        ax.set_prop_cycle(None)
        df_yt_plot.plot(ax=ax, linestyle='--')
        plt.tight_layout()
        plot_title_combined = f"{exp}"
        print(plot_title_combined)
        file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

        plt.savefig(
            "../../plots/fetch_based/temporal_watch_count/temporal_watch_count_title_search_vs_polls_ma7_" + file_name + ".png")
        # corr = df_merged.corr()
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        # fig.colorbar(cax)
        # ticks = np.arange(0, len(df_merged.columns), 1)
        # ax.set_xticks(ticks)
        # plt.xticks(rotation=90)
        # ax.set_yticks(ticks)
        # ax.set_xticklabels(df_merged.columns)
        # ax.set_yticklabels(df_merged.columns)
        # plt.tight_layout()
        # plt.show()

        df_yt_plot_v2 = df_yt_plot.rename(columns={a: a.split("_")[0] for a in df_yt_plot.columns})
        df_polls_plot_v2 = df_polls_plot.rename(columns={a: a.split("_")[0] for a in df_polls_plot.columns})

        corrwith = df_yt_plot_v2.corrwith(df_polls_plot_v2)
        corrwith_df = pd.DataFrame(corrwith).T
        corrwith_df['Avg'] = corrwith.mean()
        pd.options.display.float_format = '{:,.2f}'.format
        print(corrwith_df.to_string(index=False))
