import pandas as pd
import numpy as np
from unidecode import unidecode


# Charger les données
data = pd.read_csv("./new_file.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"

###################### Analyse par recherche ###########################

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
list_homepage = []

categories = ["ED","EG","G","D","C","O","P","EU"]
nb_homepage=[0,0,0,0,0,0,0,0]
nb=[0,0,0,0,0,0,0,0]
total_homepage = [0,0,0,0,0,0,0,0]
total = [0,0,0,0,0,0,0,0]

for i in range(0,len(data["title"])) :
    type = data["type"][i]
    if("regular" == type and i != 0):
        list.append(nb)
        list_homepage.append(nb_homepage)
        total_homepage = np.add(nb_homepage,total_homepage)
        total = np.add(nb,total)
        nb_homepage=[0,0,0,0,0,0,0,0]
        nb=[0,0,0,0,0,0,0,0]
        it+=1
        for j in range(0,8) :
            category = categories[j]
            nb[j] += data[category][i]
    elif(i == 0):
        for j in range(0,8) :
            category = categories[j]
            nb[j] += data[category][i]
            
    if ("homepage" == type):
        for j in range(0,8) :
            category = categories[j]
            nb[j] += data[category][i]
    else :
        for j in range(0,8) :
            category = categories[j]
            nb_homepage[j] += data[category][i]

    
new_data_regular = pd.DataFrame();
new_data_homepage = pd.DataFrame();
new_data_both = pd.DataFrame();

f_col = []
for i in range(0,it):
    f_col.append(str(i))
f_col.append("total")

new_data_regular["Regular"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list)[:,i]
    ar = np.append(ar,total[i])
    new_data_regular[category] = ar


new_data_homepage["Homepage"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_homepage)[:,i]
    ar = np.append(ar,total_homepage[i])
    new_data_homepage[category] = ar


new_data_total = pd.DataFrame();
new_data_total["Total"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_homepage)[:,i]
    ar = np.append(ar,total_homepage[i])
    ar2 = np.array(list)[:,i]
    ar2 = np.append(ar2,total[i])
    new_data_total[category] = np.add(ar,ar2)

# Enregistrer le DataFrame mis à jour dans le même fichier CSV
new_data_regular.to_csv("analysis_regular.csv", index=False)
new_data_homepage.to_csv("analysis_hompage.csv", index=False)
new_data_total.to_csv("analysis_total.csv", index=False)