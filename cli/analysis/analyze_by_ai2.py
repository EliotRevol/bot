import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder


# Charger les données
data = pd.read_csv("./base_ai.csv") 
data_total = pd.read_csv("./to_analyze/EQ_40.csv") 


####################### Analyse par bot ################################

categories = ["ED","EG","G","D","C","O","P","EU"]
for i in range(0,8):
    X_train = data["name"]
    y_train = data[categories[i]]
    X_total = data_total["title"]

    tfidf_vectorizer = TfidfVectorizer(max_features=10000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_total = tfidf_vectorizer.transform(data_total["title"])

    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(X_train_tfidf, y_train)

    predictions = svm_classifier.predict(X_total)

    data_total[categories[i]] = predictions


data_total.to_csv("./analyzed/search_file.csv", index=False)
