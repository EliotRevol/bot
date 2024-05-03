import re

import pandas as pd
import tqdm
from matplotlib import pyplot as plt, cycler, rcParams
from matplotlib.lines import Line2D
from sklearn.metrics import mean_absolute_error

from experiments.utils import multi_check_with_accent
from utils.const import ResultTypes, Experiments, LegislativeParties
from utils.io import dump_pickle, read_pickle, read_multi_folder, dump_json

if __name__ == '__main__':
    experiment_folder = [
        "05*"
    ]
    partySynonymType = LegislativeParties.IncreasedDetail
    partySynonymTypeStr = "IncreasedDetail" if LegislativeParties.IncreasedDetail == partySynonymType else "MinimalDetail"
    generate = True
    if generate:

        for exp in [Experiments.WELCOME_WALK,Experiments.NATIONAL_NEWS_WALK]:
            print(exp)

            # path = "/udd/ayesilka/temp_data/ayesilka/election_data/"
            path = "/media/ali/30aa46bd-4e3b-4772-b005-8cfe085f9148/home/ali/election_data/"
            experiments = read_multi_folder(experiment_folder, exp, ResultTypes.JSON, path)

            video_titles = [(" ".join(f['tags']).lower().replace("#",""), f['insertionDate'].split("T")[0]) for e in experiments for f in e if f and f['tags']]

            # Official Candidates
            candidate_dictionary = {c_: {b: 0 for b in set([a[1] for a in video_titles])} for c_ in
                                    partySynonymType}
            for candidate, snonyms in tqdm.tqdm(partySynonymType.items()):
                # candidate_lower = candidate.lower()
                # candidate_dictionary[candidate] += sum(
                #     [1 for text in video_titles if check_with_accent(candidate_lower, text.lower())])
                for text, date in video_titles:
                    if multi_check_with_accent([candidate] + snonyms, text.lower()):
                        candidate_dictionary[candidate][date] += 1

            dump_pickle("temporal_tag_search_" + exp.lower() + "_" + partySynonymTypeStr + ".pkl",
                        candidate_dictionary)
    plot = True
    if plot:
        for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
            print(exp)

            plot_title_combined = f"{exp}"
            print(plot_title_combined)
            file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
            candidate_dictionary = read_pickle(
                "temporal_tag_search_" + exp.lower() + "_" + partySynonymTypeStr + ".pkl")
            # plt.figure(figsize=(10, 5))
            fig = plt.figure(figsize=(10, 5))
            plt.title(plot_title_combined)
            for c, v in candidate_dictionary.items():
                date, Scores = zip(*sorted(zip(candidate_dictionary[c].keys(), candidate_dictionary[c].values())))
                # plt.plot(candidate_dictionary[c].keys(),candidate_dictionary[c].values())
                plt.plot(date, Scores, label=c)

            fig.axes[0].set_xticks(fig.axes[0].get_xticks()[::10])

            # normalized_polls = {a: b / (sum(Polls.round1.values())) for a, b in
            #                     Polls.round1.items()}
            # for c in candidate_dictionary:
            #     candidate_dictionary[c]['Polls'] = normalized_polls[c]
            # values = candidate_dictionary.values()
            # plt.bar(candidate_dictionary.keys(), [v / sum(values) if sum(values) > 0 else 0 for v in values])

            # df = pd.DataFrame.from_dict(candidate_dictionary)
            # df.T.plot(kind="line", stacked=True, figsize=(10, 5), title=plot_title_combined)
            plt.xticks(rotation=90)
            plt.legend()
            plt.tight_layout()
            plt.savefig(
                "../../plots/legislative/walk_based/temporal_tag_search/temporal_tag_search_" + file_name + "_" + partySynonymTypeStr + ".png")
            dump_json(
                "../../plots/legislative/walk_based/temporal_tag_search/temporal_tag_search_" + file_name + "_" + partySynonymTypeStr + ".json",
                candidate_dictionary)
            df = pd.DataFrame.from_dict(candidate_dictionary)
            df.sort_index(inplace=True)
            df.rolling(window=7).mean().plot(title=plot_title_combined, figsize=(10, 5))
            plt.tight_layout()
            plt.savefig(
                "../../plots/legislative/walk_based/temporal_tag_search/temporal_tag_search_ma7_" + file_name + "_" + partySynonymTypeStr + ".png")

    polls_comparison = True
    if polls_comparison:
        for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
            print(exp)

            plot_title_combined = f"{exp}"
            # print(plot_title_combined)
            file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)
            candidate_dictionary = read_pickle(
                "temporal_tag_search_" + exp.lower() + "_" + partySynonymTypeStr + ".pkl")
            df_yt = pd.DataFrame.from_dict(candidate_dictionary)
            # df_yt.rename(index={"14.01.2022": "01_14_2022"}, inplace=True)
            # df_yt = df_yt.drop("14.01.2022")

            # df_yt.set_index(pd.to_datetime(df_yt.index, format="%m_%d_%Y").strftime("%Y-%m-%d"), inplace=True)
            df_yt.sort_index(inplace=True)
            df_yt = df_yt.div(df_yt.sum(axis=1), axis=0)
            df_yt.rename(columns={"LREM": "Ensemble", "UDC": "LR"}, inplace=True)
            parties = df_yt.columns
            df_polls = pd.read_csv("../legislative_sondage/part1_agg.csv")
            df_polls = df_polls.set_index("Dates").sort_index()
            df_polls = df_polls.div(df_polls.sum(axis=1), axis=0)

            df_merged = pd.merge(df_polls, df_yt, left_index=True, right_index=True, how='inner',
                                 suffixes=["_Polls", "_YouTube"])
            # ----------- plot vs polls ----------
            df_polls_plot = df_merged[
                [a for a in df_merged.columns if 'Polls' in a and a.split("_")[0] in parties]]

            df_yt_plot = df_merged[
                [a for a in df_merged.columns if
                 'YouTube' in a and a.split("_")[0] in parties]]

            df_polls_plot = df_polls_plot[sorted(df_polls_plot)]
            ax = df_polls_plot.plot(figsize=(10, 6), lw=2)
            ax.set_prop_cycle(None)
            df_yt_plot = df_yt_plot[sorted(df_yt_plot)]
            df_yt_plot.plot(ax=ax, linestyle='--', lw=2)
            ax.set_prop_cycle(None)
            colors = []


            def get_prop_cycle():
                prop_cycler = rcParams['axes.prop_cycle']
                if prop_cycler is None and 'axes.color_cycle' in rcParams:
                    clist = rcParams['axes.color_cycle']
                    prop_cycler = cycler('color', clist)
                return prop_cycler


            colors = [item['color'] for item in get_prop_cycle()]
            custom_lines = [Line2D([0], [0], color=colors[i], lw=2) for i in range(len(df_yt_plot.columns))]
            legend1 = ax.legend(custom_lines, [a.split("_")[0] for a in df_yt_plot.columns], loc="upper left",
                                prop={'size': 15})

            custom_lines = [Line2D([0], [0], color="black", lw=2),
                            Line2D([0], [0], color="black", linestyle="--", lw=2),
                            ]
            legend2 = ax.legend(custom_lines, ["Polls", "YouTube", ], loc="upper right", prop={'size': 15})
            plt.gca().add_artist(legend1)

            plt.tight_layout()
            plot_title_combined = f"{exp}"
            print(plot_title_combined)
            file_name = re.sub(r"[\n\t\s]*", "", plot_title_combined)

            plt.savefig(
                "../../plots/legislative/walk_based/temporal_tag_search/temporal_tag_search_vs_polls_" + file_name + "_" + partySynonymTypeStr + ".png")
            # ----- corr mae etc ---

            df_yt_plot_v2 = df_merged[
                [a for a in df_merged.columns if
                 'YouTube' in a and a.split("_")[0] in parties]]
            df_yt_plot_v2 = df_yt_plot_v2.rename(
                columns={a: a.split("_")[0] for a in df_yt_plot_v2.columns})
            df_yt_plot_v2 = df_yt_plot_v2[sorted(df_yt_plot_v2)]

            df_polls_plot_v2 = df_merged[
                [a for a in df_merged.columns if
                 'Polls' in a and a.split("_")[0] in parties]]
            df_polls_plot_v2 = df_polls_plot_v2.rename(
                columns={a: a.split("_")[0] for a in df_polls_plot_v2.columns})
            df_polls_plot_v2 = df_polls_plot_v2[sorted(df_polls_plot_v2)]

            corrwith = df_yt_plot_v2.corrwith(df_polls_plot_v2)
            corrwith_df = pd.DataFrame(corrwith).T
            corrwith_df['Avg'] = corrwith.mean()
            pd.options.display.float_format = '{:,.2f}'.format
            print("Corr")
            print(corrwith_df.to_string(index=False))

            print("MAE")
            avg = 0
            for c in df_yt_plot_v2.columns:
                polls_plot = df_polls_plot_v2[c]
                yt_plot = df_yt_plot_v2[c]
                rmse = mean_absolute_error(polls_plot, yt_plot)
                avg += rmse
                print(f"{c}\t{rmse :.2f}")
            print(f"AVG\t{avg / len(df_yt_plot_v2.columns):.2f}")
            avg_per_day_mention = {a: sum(b.values()) / len(b.values()) for a, b in candidate_dictionary.items()}

            avg_per_day_mention_score = 0
            cand, avg_score = zip(*sorted(zip(avg_per_day_mention.keys(), avg_per_day_mention.values())))
            print("AVG mention")
            for c, a in zip(cand, avg_score):
                avg_per_day_mention_score += a
                print(f"{c}\t{a:.2f}")
            print(f"AVG\t{avg_per_day_mention_score / len(avg_score):.2f}")

    print("Finished")
