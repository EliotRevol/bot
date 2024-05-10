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
list_proposal = []
list_homepage = []
list_nbvid = [0]
list_nbproposal = [0]

categories = ["ED","EG","G","D","C","O","P","EU"]
nb_homepage=[0,0,0,0,0,0,0,0]
nb_proposal=[0,0,0,0,0,0,0,0]
nb_regular = [0,0,0,0,0,0,0,0]
total_homepage = [0,0,0,0,0,0,0,0]
total = [0,0,0,0,0,0,0,0]

for i in range(0,len(data["title"])) :
    type = data["type"][i]
    list_nbvid[it] +=1
    if("regular" == type and i != 0):
        list_nbvid.append(0)
        list_nbproposal.append(0)
        list_proposal.append(nb_proposal)
        list_homepage.append(nb_homepage)
        total_homepage = np.add(nb_homepage,total_homepage)
        total = np.add(nb_proposal,total)
        nb_homepage=[0,0,0,0,0,0,0,0]
        nb_proposal=[0,0,0,0,0,0,0,0]
        it+=1
        list_nbproposal[it]+=1
        for j in range(0,8) :
            category = categories[j]
            nb_proposal[j] += data[category][i]
            nb_regular[j] += data[category][i]
    elif(i == 0):
        list_nbproposal[it]+=1
        for j in range(0,8) :
            category = categories[j]
            nb_proposal[j] += data[category][i]
            nb_regular[j] += data[category][i]
            
    if ("homepage" == type):
        for j in range(0,8) :
            category = categories[j]
            nb_homepage[j] += data[category][i]
    else :
        list_nbproposal[it]+=1
        for j in range(0,8) :
            category = categories[j]
            nb_proposal[j] += data[category][i]

list_proposal.append(nb_proposal)
list_homepage.append(nb_homepage)
total_homepage = np.add(nb_homepage,total_homepage)
total = np.add(nb_proposal,total)
it+=1

new_data_regular = pd.DataFrame()
new_data_homepage = pd.DataFrame()
new_data_both = pd.DataFrame()

f_col = []
for i in range(0,it):
    f_col.append(str(i))


#####################Tab percent#############################
new_data_total_percent = pd.DataFrame()

new_data_total_percent["X"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_homepage)[:,i]
    ar2 = np.array(list_proposal)[:,i]  
    new_data_total_percent[category] = np.divide(np.add(ar,ar2),list_nbvid)


####################Tab percent regular#########################
new_data_regular_percent = pd.DataFrame()

new_data_regular_percent["X"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_proposal)[:,i]
    new_data_regular_percent[category] = np.divide(ar,list_nbproposal)


f_col.append("total :")

new_data_regular["Regular"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_proposal)[:,i]
    ar = np.append(ar,total[i])
    new_data_regular[category] = ar

new_data_homepage["Homepage"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_homepage)[:,i]
    ar = np.append(ar,total_homepage[i])
    new_data_homepage[category] = ar

############Tab total with total values######################
f_col.append("total stats for watched video :")
new_data_total = pd.DataFrame()
new_data_total["Total"] = f_col
for i in range(0,8):
    category = categories[i]
    ar = np.array(list_homepage)[:,i]
    ar2 = np.array(list_proposal)[:,i]
    ar = np.append(ar,total_homepage[i])
    ar2 = np.append(ar2,total[i])
    new_data_total[category] = np.append(np.add(ar,ar2),nb_regular[i])

# Enregistrer le DataFrame mis à jour dans le même fichier CSV
new_data_regular.to_csv("analysis_regular.csv", index=False)
new_data_homepage.to_csv("analysis_hompage.csv", index=False)
new_data_total.to_csv("analysis_total.csv", index=False)
new_data_total_percent.to_csv("analysis_total_percent.csv", index=False)
new_data_regular_percent.to_csv("analysis_regular_percent.csv", index=False)