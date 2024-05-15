import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./to_analyze/ED_35_8min.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"

###################### Analyse par recherche ###########################

list_ed = ["biard","rigault","virginie joron","philippe bilger","sebastien chenu","extreme droite","asselineau","le pen", "bardella","marechal","marion"," rn","zemmour","chenu","reconquete","philippot","nicolas bay","gollnish","briois","aliot","collard","menard","front national","fn","rassemblement national","patriote","reconquete","trump"]
list_eg = ["clemence guette","extreme gauche","guetté","melenchon","nupes","aubry","bompard","panot","autain","lfi","insoumis","communisme","boyard"]
list_c = ["clinton","biden","veran","macron","hayer","attal","moretti","lrem","edouard philippe","en marche",]
list_g = ["front populaire","alexis corbières","claire nouvian","francois ruffin","plenel","socialiste"," ps,"," ps ","sophia aram""le drian","glucksmann","valls","la gauche","de gauche","hollande","mitterrand"]
list_d = ["républicain"," lr ","carayon","bruno le maire","alain carignon","bellamy","francois-xavier","pecresse","la droite","de droite","balkany","republicain","larcher"]
list_p = ["la loi ","israel","ouighour","politique","diplomatie","censure","etat","fusillade","palestin","populisme","gilets jaunes","jinping","russie","diplomatie","fusillades","nazi","debat","election","poutine","attentat","palestine","palestiniens","president","gaza","lrem","nupes","sciences po","politique","rousseau","messhia","russe","russes","ukraine","trump","democratie","parlement"]
list_eu = ["europe","europeen","europeennes","bardella","glucksmann","hayer","l ue","aubry","l'ue","manon","francois-xavier","bellamy"]

data_ED=[]
data_EG=[]
data_G=[]
data_D=[]
data_C=[]
data_O=[]
data_P=[]
data_EU=[]

for i in range(0,len(data["title"])) :
    print(i)
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
    if ((ED or EG or C or G or D or EU) or any(substring in title for substring in list_p)):
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
data["P"] = data_P
data["EU"] = data_EU
data["O"] = data_O

# Enregistrer le DataFrame mis à jour dans le même fichier CSV
data.to_csv("./analyzed/search_file.csv", index=False)