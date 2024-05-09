import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder


# Charger les données
data = pd.read_csv("./ED_Autoplay85_Nbvid35_Watchtime3min.csv")  # Assurez-vous que votre fichier CSV contient deux colonnes : "texte" et "parti_politique"

# Diviser les données en ensembles d'entraînement et de test 1752 1567
X_train, X_test, y_train, y_test = train_test_split(pd.concat([data["title"][:294],data["title"][776:874],data["title"][889:933],data["title"][1567:1751]]),pd.concat([data["parti"][:294],data["parti"][776:874],data["parti"][889:933],data["parti"][1567:1751]]), test_size=0.2, random_state=42)

print(y_test)

# Encoder les étiquettes de classe
label_encoder = LabelEncoder()
label_encoder.fit(["ED","EU","O","P","EG","C"])
y_train_encoded = label_encoder.transform(y_train)
y_test_encoded = label_encoder.transform(y_test)



# Créer une représentation TF-IDF des données textuelles
tfidf_vectorizer = TfidfVectorizer(max_features=10000)  # Vous pouvez ajuster le nombre maximum de fonctionnalités selon vos besoins
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)
X_total = tfidf_vectorizer.transform(data["title"])

# Entraîner un modèle SVM
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X_train_tfidf, y_train_encoded)

# Faire des prédictions sur l'ensemble de test
predictions = svm_classifier.predict(X_total)

print(predictions)
print(label_encoder.classes_)

predictions_original = label_encoder.inverse_transform(predictions)

# Ajouter une nouvelle colonne dans le DataFrame pour stocker les prédictions
data["pred_parti"] = predictions_original

# Enregistrer le DataFrame mis à jour dans le même fichier CSV
data.to_csv("new_file.csv", index=False)
