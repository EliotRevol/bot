# Bot Crawler

## Description
    Utilitaire python permettant de lancer des bots qui au moyen d'une liste d'événements
    vont exécuter des actions sur Youtube.

## Prérequis
* Docker
* Python 3
* Pip

## Installation

$> `cd bot && docker image build -t bot .`  
$> `cd ..`  
$> `cd cli && pip3 install -r requirements.txt`

## Lancement rapide

$> `cd cli`  
$> `python3 main.py`

## Lancement Paramétré

Deux options sont paramétrable pour le moment :
* Le répertoire de sortie des résultats
* La liste d'événements

### Arguments

#### Filename

$> `python3 main.py --filename <output_filename> `

#### Cookies

$> `python3 main.py --cookie <cookie_filename> `

### Fonction Référence

#### runJob

| Name   | Type |      Value      |  Required | Description |
|----------|-----|:-------------:|:------:|----------|
| `events` |string| | **True** | Liste d'évènements comme décris plus loin |
| `user_agent` |string| | **True** | userAgent |
| `width` |int| 0-8000 | **True** | Largeur de l'écran en pixels |
| `height` |int| 0-8000 | **True** | Hauteur de l'écran en pixels |
| `cookies` |string| | **True** | Nom du fichier contenant les cookies |

#### generate_user_agent_and_resolution

Génère un user agent et une taille d'écran aléatoirement.

#### save_json

Sauvegarde les résultat dans un fichier JSON

| Name   | Type |      Value      |  Required | Description |
|----------|-----|:-------------:|:------:|----------|
| `set` |json| | **True** | Résultats obtenues après un runJob |
| `out_folder`|string |   | **True** | Chemin du dossier de résultats |
| `filename`|string |   | **False** | Nom du fichier d'enregistrement des résultat si `None` timestamp |

#### save_csv

Sauvegarde les résultat dans un fichier CSV

| Name   | Type |      Value      |  Required | Description |
|----------|-----|:-------------:|:------:|----------|
| `set` |json| | **True** | Résultats obtenues après un runJob |
| `out_folder`|string |   | **True** | Chemin du dossier de résultats |
| `filename`|string |   | **False** | Nom du fichier d'enregistrement des résultat si `None` timestamp |

#### get_randoms_videos

Requête a l'api Youtube d'un ou plusieurs identifiant aléatoire de vidéo existante

| Name   | Type |      Value      |  Required | Description |
|----------|-----|:-------------:|:------:|----------|
| `nb_required` |int|0-100 | **True** | Nombre de vidéo random demandées |

#### populate_ytkids

Proxy Youtube Kids résolvant un csv

| Name   | Type |      Value      |  Required | Description |
|----------|-----|:-------------:|:------:|----------|
| `filepath` |dtring| | **True** | Fichier csv à résoudre |


### Répertoire de sortie

* Ouvrir le fichier : `cli/main.py`
* Modifier la valeur de la variable `out_path`

#### Parser le json

``` { .py }
import json,ast

with open(filename) as f:
        data = f.read()
        data_json = ast.literal_eval(data)
```

### Liste d'évènements
Pour modifier la liste des évènement :
Ouvrir le fichier `cli/main.py`, puis modifier la variable `events`.

    events = ['{"type": "fetch", "searchSelection":3}',
            '{"type": "watchOne", "video_id": "jSZkYrtpZoY", "searchTerm":"Les druides - Prêtres des peuples celtes | ARTE", "watchTime": 60000}',
            '{"type": "autoplay", "searchSelection": 3, "watchTime": 60000}',
            '{"type": "fetch", "searchSelection":3}'
        ]

Quatre évènements sont possible. Il peuvent être combinés et répété.

**Remarque** : L'évènement "autoplay" doit toujours être précédé de l'évènement "watchOne"

##### Paramètres des évènements
###### fetch
Cet évènement récupère toute la homepage un nombre de fois paramétré.

| Name              | Type   | Value | Required | Description                 |
|-------------------|--------|:-----:|:--------:|-----------------------------|
| `type`            | string | fetch | **True** | Job type                    |
| `searchSelection` | int    | 0-100 | **True** | Nombre de fetch de homepage |

###### watchOne
Cet évènement regarde une vidéo

| Name         | Type   |  Value   | Required  | Description                                                                       |
|--------------|--------|:--------:|:---------:|-----------------------------------------------------------------------------------|
| `type`       | string | watchOne | **True**  | Job type                                                                          |
| `video_id`   | string |          | **True**  | Id de la vidéo à regarder                                                         |
| `searchTerm` | string |          | **True**  | Titre de la vidéo à regarder                                                      |
| `watchTime`  | int    | 0-100000 | **True**  | Temps en millisecondes de visionnage                                              |
| `alea`       | int    | 0-100000 | **False** | Temps en millisecondes d’aléa sur le visionnage (doit être inférieur à watchTime) |

###### autoplay
Cet évènement fais une boucle de visionnage sur la première suggestion de vidéo.

**Toujours lancer cet évènement après un "watchOne"**


| Name              | Type   |  Value   | Required  | Description                                                                       |
|-------------------|--------|:--------:|:---------:|-----------------------------------------------------------------------------------|
| `type`            | string | autoplay | **True**  | Job type                                                                          |
| `searchSelection` | int    |  0-100   | **True**  | Nombre de vidéo visionnées en autoplay                                            |
| `watchTime`       | int    | 0-100000 | **True**  | Temps en millisecondes de visionnage par vidéo                                    |
| `alea`            | int    | 0-100000 | **False** | Temps en millisecondes d’aléa sur le visionnage (doit être inférieur à watchTime) |

###### fetchAutoplay
Même évenement que autoplay mais fais un fetch de la homepage avant chaque visionnage de vidéo.

**Toujours lancer cet évènement après un "watchOne"**


| Name              | Type   |  Value   | Required  | Description                                                                       |
|-------------------|--------|:--------:|:---------:|-----------------------------------------------------------------------------------|
| `type`            | string | autoplay | **True**  | Job type                                                                          |
| `searchSelection` | int    |  0-100   | **True**  | Nombre de vidéo visionnées en autoplay                                            |
| `watchTime`       | int    | 0-100000 | **True**  | Temps en millisecondes de visionnage par vidéo                                    |
| `alea`            | int    | 0-100000 | **False** | Temps en millisecondes d’aléa sur le visionnage (doit être inférieur à watchTime) |

###### channelSniffer
Cet évènement regarde un nombre donné de vidéo aléatoire provenant d'une chaîne spécifiée.

| Name              | Type   |     Value      | Required  | Description                                                                       |
|-------------------|--------|:--------------:|:---------:|-----------------------------------------------------------------------------------|
| `type`            | string | channelSniffer | **True**  | Job type                                                                          |
| `channel_id`      | string |    **(*)**     | **True**  | partie de url de la chaîne **(*)**                                                |
| `searchTerm`      | string |                | **True**  | Nom de la chaîne                                                                  |
| `searchSelection` | int    |     0-100      | **True**  | Nombre de vidéo visionnées alétoirement de la chaîne                              |
| `watchTime`       | int    |    0-100000    | **True**  | Temps en millisecondes de visionnage par vidéo                                    |
| `getAll`          | int    |   true-false   | **True**  | Récupérer toutes les vidéos de la chaîne                                          |
| `alea`            | int    |    0-100000    | **False** | Temps en millisecondes d’aléa sur le visionnage (doit être inférieur à watchTime) |

**(*) Exemple : https://www.youtube.com/user/FRDeath360 video_id = "/user/FRDeath360"**

Pour retourner des infos sur les vidéos du channel, utiliser `getAll`:
> '{"type": "channelSniffer", "searchSelection": 0, "channel_id": "/user/HG13710", "searchTerm":"Gerard Heiries", "getAll": true}',
### CLI V2
Inside `cli` folder, `main-generic-elections.py` (refactored version of `main-plan-expes.py`allows arguments to be passed as json or/and argparse string. The experiments for elections 2022 are implemented by using this file. 
####Mappings with Old cli
Channels json inside `main-plan-expes.py` are extracted to `channels.json`.

All parameters for the experiments inside the code are removed and set from outside by using a json file (see `sample_config.json`)  or by using argument string (see `main-generic-elections.py` arguments for details)
Parameters from argument string will override the parameters from json file.

In order to run by using a config.json file to read parameters.

$> `python main-generic-elections.py --config sample_config.json` 

If you want to override just one parameter (`experiment`) from config by giving argparse parameter.

$>` python main-generic-elections.py --config sample_config.json --experiment election-welcome-walk`
## Experiments
Experiments are grouped as Generic, and Election,Meta. Generic experiments are similar to the election's, yet they have the fix naming convention for the previous work.
Experiments create 3 fixed 2 optional files upon completion. 3 fixed files are CSVs and JSONs for the output of the experiments and `_vars.txt` for variables. 2 optional files are ending with `_transcript.gz` and `_html.gz` generated by defining a language on `transcript_language` param and `save_html` parameter respectively. See [cli/sample_config.json](cli/sample_config.json) for an example of fetching French transcripts.  
### Elections experiments
Currently, 5 different election experiments are implemented.

All of them requires `experiment` parameter to be set, additionally each of them requires different parameters, as follows:

`Walk` experiments can save html in order to do it you can set `save_html` as true in config.json or `--save_html` in argparse.

Also, they can save transcripts, to make it `transcript_language` should be defined as json array for the languages which transcripts are expected to save.

Lastly, `lang` parameter will set browser language for all the experiments, but it is optional and default will be set to `en`


| Name                               | Description                                                                                                                                   | Required Params           |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| `election-welcome-fetch`           | Fetch welcome page in every given time period                                                                                                 | waiting_seconds           |
| `election-welcome-walk`            | Fetch welcome page, start and watch videos from recommendations                                                                               | nb_runs,nb_walks          |
| `election-national-news-fetch`     | Fetch national news <a href="https://www.youtube.com/channel/UCcE169gw8kJCzyCJZXb7DQw">page</a> in every given time period                    | waiting_seconds           |
| `election-national-news-walk`      | Fetch national news <a href="https://www.youtube.com/channel/UCcE169gw8kJCzyCJZXb7DQw">page</a> , start and watch videos from recommendations | nb_runs,nb_walks          |
| `election-channel-personalization` | Watch videos from randomly selected channel, then fetches recommendations and welcome page                                                    | nb_runs,nb_walks,channels |

### Meta Experiments
Similar to the `election-national-news-walk` and `election-channel-personalization` experiments 2 type of experiments implemented, named meta-walk and meta-channel personalization starting from selected meta channels. See [meta channels](cli/meta_channels.json).   

| Name                                | Description                                                                                                                          | Required Params            |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| `meta-walk`                         | Fetch welcome page, go to the randomly selected channel, then watch videos and fetch recommendations from proposals and welcome page | nb_runs,nb_walks           |
| `meta-channel-personalization-walk` | Watch videos from randomly selected channel, then fetches recommendations and welcome page                                           | nb_runs,nb_walks, channels |

***
# Backups
To backup the experiments data across machines set a crontab on [backup/backup_generic.sh](backup/backup_generic.sh) 
# GUI
There are 2 GUI webpages developed in this project. GUI Half life is the webpage for calculating the cosine distance between the given YouTube channel and the prefetched reference videos using prefetched mainstream vectors.
GUI is the webpage developed for French Presidential Elections '22 (See https://elections.whosban.eu.org). 

## GUI Half Life
In order to run GUI Half Life, first "bot" docker image should be built 

$> `cd bot && docker image build -t bot .`

Then, run the sh script for building the image and creating the container instance gui-half-life. 

$> `sh gui_half_life.sh`

Webpage is hosted on 5000 port.

**Optional:** To create certificates (as in GUI below) modify [cert_create.sh](cert_create.sh).
To modify ports and nginx configurations for https see [gui_half_life/nginx_config/gui_half_life](gui_half_life/nginx_config/gui_half_life).

### Configuration
#### Background Jobs (Crontab - Prefetch Mainstream and Reference Videos)
See [gui_half_life/regeneration/crontab.sh](gui_half_life/regeneration/crontab.sh).
Generated vectors are stored in [gui_half_life_data/vectors](gui_half_life_data/vectors).
#### Walks started from webpage
Exported walks are stored in [gui_half_life_data/vectors](gui_half_life_data/walks).

#### Backup of the walks and vectors
Set a crontab (must be 1 per day for naming convention) for calling script [backup/backup_gui_half_life_data.sh](backup/backup_gui_half_life_data.sh)

#### Logs
Logs are stored inside [logs_half_life](logs_half_life) folder. Check flask_prod.log and nginx logs for details.

## GUI

Run the script for building the image and creating the container instance gui.

$> `sh gui.sh`

To renew certificates 

$> `sh cert_create.sh` script could be used or modified.

### Configuration
#### Background Jobs (Crontab - Generating Daily Analytics For Plots)
See [gui/regeneration/crontab.sh](gui/regeneration/crontab.sh)
Generated data for the plots are stored in [gui_data/plot_data](gui_data/plot_data).

#### Logs
Logs are stored inside [logs](logs) folder. Check flask_prod.log and nginx logs for details.

# Election Analytics
See [election/README.MD](election/README.MD)