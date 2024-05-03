from ast import literal_eval

import holoviews
import pandas as pd
from holoviews import Chord, dim
from matplotlib import pyplot as plt
from panel import panel

from utils.const import Experiments

# matplotlib.use('TkAgg')

holoviews.extension('bokeh')
# holoviews.extension('matplotlib')

holoviews.output(size=300)
if __name__ == '__main__':
    # pd.set_option('display.max_columns', None)  # or 1000
    # pd.set_option('display.max_rows', None)  # or 1000
    # pd.set_option('display.max_colwidth', None)  # or 199
    for exp in [Experiments.NATIONAL_NEWS_WALK]:
        # for exp in [Experiments.WELCOME_WALK, Experiments.NATIONAL_NEWS_WALK]:
        path = f"watch_count_date_{str(exp)}_2022.csv"
        print(exp)
        df = pd.read_csv(path)
        print(f"Read: {path}")
        df = df.drop("like", axis=1)
        c = df.groupby("Title").count().reset_index()[['Title', 'Candidate_Name']]
        c.rename(columns={"Candidate_Name": "Recommended_Count"}, inplace=True)
        merged_df = pd.merge(df, c, how="left", on="Title")
        print(merged_df.cov())
        print(merged_df.corr())
        plots = False
        if plots:
            df.loc[pd.isna(df["Initial_Candidate_Clicked"]), "Initial_Candidate_Clicked"] = "[""]"
            df['Initial_Candidate_Clicked'] = df['Initial_Candidate_Clicked'].apply(
                literal_eval)  # convert to list type
            df = df.explode("Initial_Candidate_Clicked")
            candidates = sorted(df['Candidate_Name'].unique())
            # print(candidates)
            # print(f"{df.corr().iloc[0, 1]:.2f}")

            watch_count_per_hour_dict = {
                candidate: {"Watch_Count - Hours": df[df['Candidate_Name'] == candidate].corr().iloc[0, 1]} for
                candidate in
                candidates}
            watch_count_per_hour_dict["All"] = {"Watch_Count - Hours": df.corr().iloc[0, 1]}

            e = df.groupby("Title").agg(
                {"Watch_Count": ["count", "sum"], "Hours_After_Upload": ["sum", "count"]}).reset_index()
            e['Watch_Count_per_Hours'] = e['Watch_Count']['sum'] / e['Hours_After_Upload']['sum']

            # watch_count_per_hour_dict['All']["Watch_Count/Hours - Count"] = \
            #     e.corr()['Watch_Count_per_Hours']['Watch_Count']['count']
            #
            # for c in candidates:
            #     e = df[df['Candidate_Name'] == c].groupby("Title").agg(
            #         {"Watch_Count": ["count", "sum"], "Hours_After_Upload": ["sum", "count"]}).reset_index()
            #     e['Watch_Count_per_Hours'] = e['Watch_Count']['sum'] / e['Hours_After_Upload']['sum']
            #     watch_count_per_hour_dict[c]["Watch_Count/Hours - Count"] = \
            #         e.corr()['Watch_Count_per_Hours']['Watch_Count']['count']

            plt.figure(figsize=(8, 6))

            plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees
            plot_df = pd.DataFrame(watch_count_per_hour_dict)
            ax = plot_df.T.plot(y="Watch_Count - Hours", kind="bar", legend=False, title=exp)

            plt.tight_layout()
            plt.savefig(f"eda/bar-watch_count_hours_corr_{exp}.png")

            chord_df = df[['Candidate_Name', 'Initial_Candidate_Clicked']]
            chord_df.Initial_Candidate_Clicked.fillna("Others", inplace=True)
            crosstab_df = chord_df.groupby(["Candidate_Name", "Initial_Candidate_Clicked"]).size().reset_index().rename(
                columns={0: "value", "Candidate_Name": "target", "Initial_Candidate_Clicked": "source"})
            labels = pd.DataFrame(
                {"Names": crosstab_df.source.unique(), "Group": [0 for a in crosstab_df.source.unique()]})
            d = {value: i for i, value in enumerate(list(crosstab_df.source.unique())
                                                    )}


            def str2num(s):
                return d[s]


            crosstab_df['source'] = crosstab_df['source'].apply(str2num)
            crosstab_df['target'] = crosstab_df['target'].apply(str2num)
            labels_ds = holoviews.Dataset(pd.DataFrame(labels), 'index')
            chord = Chord((crosstab_df, labels_ds)).opts(cmap='Category20', edge_cmap='Category20',
                                                         edge_color=dim('source').str(),
                                                         labels='Names', node_color=dim('index').str())

            panel(chord).show()
