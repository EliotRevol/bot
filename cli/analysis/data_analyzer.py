import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./ED_Autoplay85_Nbvid35_Watchtime3min.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"

###################### Analyse par recherche ###########################

list_ed = ["le pen", "bardella","marechal","marion","rn"]
list_eg = ["melenchon"]
list_c = ["macron","hayer"]
list_g = ["glucksmann","valls"]
list_d = []
list_p = ["debat","election","poutine","attentat"]
list_eu = ["europe","europeen","europeenne","bardella","glucksmann","hayer"]

nb_ED=0
nb_EG=0
nb_G=0
nb_D=0
nb_C=0
nb_O=0
nb_P=0
nb_EU=0
it = 0
list = []

categories = ["ED","EG","G","D","C","O","P","EU"]
nb_homepage=[0,0,0,0,0,0,0,0]
nb=[0,0,0,0,0,0,0,0]
total_homepage = [0,0,0,0,0,0,0,0]
total = [0,0,0,0,0,0,0,0]

for i in range(0,len(data["title"])) :
    type = data["type"][i]
    if(type is "regular"):
        list.append([])
        it+=1
        #anything
    if (type is "homepage"):
        for j in range(0,8) :
            category = categories[j]
            nb[j] += data[category][i]
    else :
        for j in range(0,8) :
            category = categories[j]
            nb_homepage[j] += data[category][i]

    

data["ED"] = data_ED
data["EG"] = data_EG
data["G"] = data_G
data["D"] = data_D
data["C"] = data_C
data["O"] = data_O
data["P"] = data_P
data["EU"] = data_EU

# Enregistrer le DataFrame mis à jour dans le même fichier CSV
data.to_csv("new_file.csv", index=False)