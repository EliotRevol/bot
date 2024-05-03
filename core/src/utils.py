## @package utils
#  Module utilitaire
import gzip
import json
import pickle
from enum import Enum

import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

from core.src import config
from core.src.export import save_json, save_csv


class Status(str, Enum):
    NO_EN = "UnavailableLanguage"
    OK = "ValidTranscript"
    NO_TRANSCRIPT = "NoTranscript"
    ERROR = "Error"
    UNAVAILABLE = "Unavailable"


def read_json(path):
    with open(path) as f:
        return json.load(f)

def read_pickle(path):
    with open(path,"rb") as f:
        return pickle.load(f)

def dump_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


## Sauve les résultats et les variables d'expérience
# @param vars variable d'expérience
# @param res résultat de l'éxpérience
# @param out_path Chemin des fichier résultat
# @param filename Nom des fichiers résultats
def fetch_transcripts(res, filename, cookies, transcript_language, store_folder=None):
    urls = [a['url'] for a in res if a['type'] == "regular"]
    transcripts = []
    for url in urls:
        transcript = ""
        try:
            video_id = url.replace("https://www.youtube.com/watch?v=", "")
            transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, cookies=cookies,
                                                             languages=transcript_language)
            status = Status.OK
        except youtube_transcript_api.NoTranscriptFound:
            status = Status.NO_EN
        except youtube_transcript_api.NoTranscriptAvailable:
            status = Status.NO_TRANSCRIPT
        except youtube_transcript_api.TranscriptsDisabled:
            status = Status.UNAVAILABLE
        except Exception as e:
            status = Status.ERROR
        transcripts.append({'url': url, "transcript": transcript, 'status': str(status)})
    with gzip.open(config.get_output_base_name(filename, store_folder) + "_transcript.gz", 'wt', encoding="utf-8") as f:
        json.dump(transcripts, f)


def dump(vars, res, filename, save_html, cookie, transcript_language, store_folder=None):
    """
    Dumps global variables and results to json, csv and zip files.
    :param store_folder: which folder to store, default None redirects to config.OUTPUT
    :param vars: Global variables. Results and html's are deleted before export
    :param res: Bot response
    :param filename: Base name to export files
    :param save_html: Boolean flag to save html
    :param cookie: Can be used to fetch transcripts is true, Not required
    :param transcript_language: Languages to extract transcripts
    :return: csv_path
    """
    out_file_base_name = config.get_output_base_name(filename, store_folder)
    if save_html:
        html_json = [{'url': a['url'], 'html': a['bodyHtml']} for a in res if a['bodyHtml'] != ""]
        with gzip.open(out_file_base_name + "_html.gz", 'wt', encoding="utf-8") as f:
            json.dump(html_json, f)
    if transcript_language and len(transcript_language) > 0:
        fetch_transcripts(res, filename, cookie, transcript_language, store_folder)

    save_json(res, filename, store_folder)
    csv_path = save_csv(res, filename, store_folder)

    with open(out_file_base_name + "_vars.txt", 'w') as f:
        if "html_json" in vars.keys():  # huge data structure, exported as zip
            vars.pop("html_json")
        if "res" in vars.keys():
            vars.pop("res")  # alredy exported as json
        if "result" in vars.keys():
            vars.pop("result")
        f.write(str(vars))
    return csv_path
