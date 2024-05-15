import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./analyzed/search_file.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"
data_out = pd.DataFrame(columns=data.columns)
to_takeH = 25
to_takeP = to_takeH
#data_out_ = []

for i in range(0,len(data["title"])) :
    type = data["type"][i]

    if("regular" == type) : 
        to_takeH=25
        to_takeP=25
        data_out.loc[len(data_out)] = data.iloc[i]

    if(to_takeH>0 and type == "homepage"):
        to_takeH-=1
        data_out.loc[len(data_out)] = data.iloc[i]
        
    if(to_takeP>0 and type == "proposal"):
        to_takeP-=1
        data_out.loc[len(data_out)] = data.iloc[i]

#data_out = data_out_
data_out.to_csv("./analyzed/reduce.csv", index=False)