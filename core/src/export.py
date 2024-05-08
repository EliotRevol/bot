import json
import re
from copy import deepcopy
from datetime import datetime
from io import StringIO

import pandas as pd

from core.src import config


## @package export
#  Module d'export JSON et CSV

def save_csv(set, filename, store_folder=None):
    """
    Saves result as csv
    :param set: set Vidéos JSON list
    :param filename: Nom du fichier csv
    :return: Chemin du fichier csv
    """
    dateTimeObj = datetime.now()
    if filename == None:
        filename = str(dateTimeObj)
    return exportSet(set, filename, store_folder)


def save_json(set, filename, store_folder=None):
    """
    Saves result as json
    :param set: Vidéos JSON list
    :param filename: Nom du fichier json
    :return: Chemin du fichier csv
    """
    dateTimeObj = datetime.now()
    if filename == None:
        filename = str(dateTimeObj)

    items = deepcopy(set)
    [a.pop('bodyHtml', None) for a in
     items]  # remove body html from json export, they will be exported on compressed file
    with open(config.get_output_base_name(filename, store_folder) + '.json', 'w') as f:
        json.dump(items, f)


## Formatage de la liste de vidéos avant enregistrement.
# @param Videos JSON list
# @return Vidéo JSON list
def getVideos(videos):
    for video in videos:
        url = video['url']
        m = re.search('(?<=v=).*(?<=&)', url)
        if m is None:
            video_id = url[url.rfind('v=') + 2:]
        else:
            t = m.group(0)
            video_id = t[:-1]
        video['ytkids'] = 'NA'
        video['regionAllowed'] = ''
        video['url'] = video_id
        parent = video['parent_id']
        video['parent_id'] = parent[parent.rfind('v=') + 2:]
    return videos


## Exporte une liste vidéos json en fichier csv
# @param set Videos JSON list
# @param path Chemin du fichier csv
# @param filename Nom du fichier csv
def exportSet(set, filename, store_folder=None):
    flat_list = getVideos(set)
    df = pd.read_json(StringIO(json.dumps(flat_list)), orient='records')

    if not df.empty:
        csv_path = config.get_output_base_name(filename, store_folder) + '.csv'
        df.to_csv(csv_path, index=None,
                  columns=["url", "title", "author", "type", "insertionDate", "refreshNB",
                            "watchTime", "actionNB", "videoViewsNB", "parent_id"])
        return csv_path
    else:
        return None
