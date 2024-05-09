import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./ED_Autoplay85_Nbvid35_Watchtime3min.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"

###################### Analyse par recherche ###########################

list_ed = ["le pen", "bardella","marechal","marion","rn"]
list_eg = ["melenchon","nupes"]
list_c = ["macron","hayer","attal"]
list_g = ["glucksmann","valls"]
list_d = ["bellamy","francois-xavier"]
list_p = ["debat","election","poutine","attentat","palestine","palestiniens","president","gaza","lrem","nupes","sciences po","politique"]
list_eu = ["europe","europeen","europeenne","bardella","glucksmann","hayer","l ue","aubry","l'ue","manon","francois-xavier","bellamy"]

data_ED=[]
data_EG=[]
data_G=[]
data_D=[]
data_C=[]
data_O=[]
data_P=[]
data_EU=[]

for i in range(0,len(data["title"])) :
    title = data["title"][i]
    author = data["author"][i]
    title = unidecode(str.lower(title))
    author = unidecode(str.lower(author))
    ED,EG,G,D,C,O,P,EU = 0,0,0,0,0,0,0,0
    if any(substring in title or substring in author for substring in list_ed):
        ED = 1
    if any(substring in title or substring in author for substring in list_eg):
        EG = 1
    if any(substring in title or substring in author for substring in list_c):
        C = 1
    if any(substring in title or substring in author for substring in list_g):
        G = 1
    if any(substring in title or substring in author for substring in list_d):
        D = 1
    if any(substring in title or substring in author for substring in list_eu):
        EU = 1
    if ((ED or EG or C or G or D) or any(substring in title for substring in list_p)):
        P = 1
    else:
        O = 1
    
    data_ED.append(ED)
    data_EG.append(EG)
    data_G.append(G)
    data_D.append(D)
    data_C.append(C)
    data_O.append(O)
    data_P.append(P)
    data_EU.append(EU)

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