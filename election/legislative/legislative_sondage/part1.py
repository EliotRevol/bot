from datetime import timedelta

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def datetime_range(start=None, end=None):
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)


def group_weighted_mean_factory(df: pd.DataFrame, weight_col_name: str):
    # Ref: https://stackoverflow.com/a/69787938/
    def group_weighted_mean(x):
        try:
            return np.average(x, weights=df.loc[x.index, weight_col_name])
        except ZeroDivisionError:
            return np.average(x)

    return group_weighted_mean


if __name__ == '__main__':
    df = pd.read_csv("wiki.csv")
    split = df.Duration.str.split("-", expand=True)

    end_month = split[1].str.replace('[^a-zA-Z]', '', regex=True)
    end_day = split[1].str.split(" ").str[0]
    begin_month = split[0].str.replace('[^a-zA-Z]', '', regex=True)
    begin_day = split[0].str.split(" ").str[0]

    begin_month[begin_month == ""] = end_month[begin_month[begin_month == ""].index]
    begin_month = begin_month.sort_index()

    end_date = pd.to_datetime(end_month.str.cat(end_day.str.zfill(2), "2022"), format='%b%Y%d')
    begin_date = pd.to_datetime(begin_month.str.cat(begin_day.str.zfill(2), "2022"), format='%b%Y%d')

    parties = df.columns.drop(["Company", "Duration", "Size"])
    agg_polls = []

    for i, row in df.iterrows():
        for a in datetime_range(begin_date[i], end_date[i]):
            agg_polls.append([a, row["Size"]] + row[parties].values.tolist())
    agg_df = pd.DataFrame(agg_polls, columns=['Dates', "Size"] + parties.values.tolist())

    # mean_agg = agg_df.groupby("Dates").mean().reset_index()
    # mean_agg.set_index("Dates").plot(kind="line")
    #
    # plt.show()
    #
    # group_weighted_mean = group_weighted_mean_factory(df, "Size")
    # g = agg_df.groupby("Dates")  # Define
    # agg = g.agg(group_weighted_mean)
    # agg.reset_index()
    # agg.set_index("Dates").plot(kind="line")
    #
    # plt.show()
    #
    #
    #
    agg_df = agg_df.groupby("Dates").apply(
        lambda x: pd.Series(np.average(x[parties], weights=x["Size"], axis=0), parties))
    agg_df.to_csv("part1_agg.csv")
    agg_df.plot(kind="line")
    plt.savefig("legislative.png")
