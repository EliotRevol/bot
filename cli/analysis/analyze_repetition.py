import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./to_analyze/ED_35.csv")
data_out = pd.DataFrame()

d_out = []
d_out_val = []

for i in range(0, len(data["title"])):
    value = data["title"][i].strip()
    value = value.replace(" ","")
    value = value.replace("’","")
    value = value.replace("\"","")
    made = 0

    for j in range(0,len(d_out)):
        if d_out[j] == value : 
            d_out_val[j] += 1
            made = 1
    
    if (made == 0) :
        d_out.append(value)
        d_out_val.append(1)

arg_sort = np.argsort(d_out_val)
nd_out = []
nd_out_val = []
total_calc = 0

for i in range(0,len(d_out)):
    k = d_out_val[arg_sort[i]]
    nd_out.append(d_out[arg_sort[i]])
    nd_out_val.append(k)
    if(k > 1):
        total_calc += (k-1)

nd_out_val.append(total_calc)
nd_out_val.append(len(arg_sort))
nd_out_val.append(len(data["title"]))
nd_out.append("Total number or repetition : ")
nd_out.append("Unique videos : ")
nd_out.append("Total videos : ")

data_out["title"] = nd_out
data_out["number"] = nd_out_val
data_out.to_csv("./analyzed/repetition.csv", index=False)