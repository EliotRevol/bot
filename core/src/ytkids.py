import requests
import pandas as pd
from pandarallel import pandarallel

# pandarallel.initialize()
cookies = {
    'G_ENABLED_IDPS': 'google',
    'YSC': 'ECC4oOxFF-4',
}

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Visitor-Id': 'CgtoWGIyMlgwOFcxYyiwt6WABg%3D%3D',
    'Origin': 'https://www.youtubekids.com',
}

params = (
    ('key', 'AIzaSyBbZV_fZ3an51sF-mvs5w37OqqbsTOzwtU'),
)

## @package ytkids
# Proxy Youtube Kids

## Résout la catégorie d'un vidéo a partir d'un id
# @param id Vidéo id
# @return ytkids catégorie
def resolv(id):
    # print(id)
    try:
        if not isinstance(id, str) or not id:
            return "false"
        if callApi(id,'KIDS_CORPUS_PREFERENCE_PRESCHOOL') == 'OK':
            return 'petit'
        elif callApi(id,'KIDS_CORPUS_PREFERENCE_YOUNGER') == 'OK':
            return 'moyen'
        elif callApi(id,'KIDS_CORPUS_PREFERENCE_TWEEN') == 'OK':
            return 'grand'
        return 'false'
    except Exception as e:
        return 'NA'


## Appel a l'api youtube kids pour savoir si la vidéo correspond a la catégorie demandée.
# @param id Vidéo id
# @param cat categorie
# @return OK ou empty
def callApi(id, cat):
    data = '{"videoId":"'+id+'","context":{"client":{"clientName":"WEB_KIDS","clientVersion":"2.1.3","kidsAppInfo":{"contentSettings":{"corpusPreference":"'+cat+'","kidsNoSearchMode":"YT_KIDS_NO_SEARCH_MODE_OFF"}}}}}'
    response = requests.post('https://www.youtubekids.com/youtubei/v1/player', headers=headers, params=params, cookies=cookies, data=data,timeout=10)
    return (response.json()['playabilityStatus']['status'])

## Applique la résolution sur un dataframe
# @param df dataframe
# @return Dataframe résolut
def csvReso(df):
    data = []
    df['ytkids'] = df.parallel_apply(
        lambda row: resolv(row['url']),
        axis=1
    )
    return df

## Lis un fichier CSV et le transforme en DataFrame
# @param filename Nom du fichier CSV
# @return Dataframe
def readDataset(filename):
    df = pd.read_csv(filename)
    return df

## Sauvegarde le dataset dans un fichier CSV
# @param df Dataset
# @param filename Nom du fichier CSV
# @return Vidéo json
def saveDataset(df, filename):
    df.to_csv (filename, index=None)

## Remplis le champs ytkids d'un fichier CSV
# @param file fichier CSV
# @return Vidéo json
def populate_ytkids(file):
    df = readDataset(file)
    df = csvReso(df)
    saveDataset(df, file)
