import glob

import pandas as pd
import datetime


def get_time(date):
    h, m, s = date.split(":")
    return int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())


if __name__ == '__main__':
    files = glob.glob("*.csv")
    df_list = []
    for f in files:
        df = pd.read_csv(f, skiprows=5, sep=";", encoding="ISO-8859-1")
        df['duration'] = df['Total période (durée)'].apply(get_time)
        df = df.groupby("Candidat").sum("duration").reset_index()
        df['channel'] = f.split("_")[-1].split(".")[0]
        df_list.append(df)
    concat = pd.concat(df_list)
    print(concat)
    concat.to_csv("0_16_csa_tv.csv", index=False, encoding="utf-8")
