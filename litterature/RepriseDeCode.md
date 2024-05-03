## Description du logiciel
Bot crawler est un outil en ligne de commande permettant de simuler les action d'un utilisateur sur Youtube.

Il est composé de deux partie :
* Bot
* Cli

La première écrite en TypeScript est un agrégat d'action et de liste d'action faisable sur Youtube.

La deuxième est une surcouche en python permettant de lancer des liste d'action, de manipuler les résultats et de faire quelques appels à l'api Youtube.

## Technologies utilisées
### Bot
La librairie choisie pour contrôler un navigateur est Puppeteer.

Puppeteer est une bibliothèque de node.js qui fournit une API de haut niveau pour contrôler Chrome ou Chromium en headless via le protocole DevTools.

En addition à Puppeteer la librairie : puppeteer-extra-plugin-stealth à été utilisée afin de cacher au mieux à Youtube que le navigateur est automatisé.

### Cli
Librairie Python
* pandas
* google-api-python-client
* requests
* pandarallel

## Fonctionnement des différentes composantes
### Cli (Python)

Voir la doc : https://wide.gitlabpages.inria.fr/bot-crawler/

### Bot (TypeScript)

Le bot à été implémenter de façon à ce qu'il soit générique et que l'on puisse facilement l'étendre à un autre site que Youtube.

Le bot est un container qui est lancé par Cli. Il prend en entré une liste d'évènements.
Par exemple :
```
[      '{"type": "fetch", "searchSelection":3}',
        '{"type": "watchOne", "video_id": "jSZkYrtpZoY", "searchTerm":"Les druides - Prêtres des peuples celtes | ARTE", "watchTime": 6000}',
        '{"type": "fetchAutoplay", "searchSelection": 3, "watchTime": 6000}',
        '{"type": "fetch", "searchSelection":3}'
]
```
L'attribut type correspond au nom du job que le bot va lancer. Plus précisément dans le code le bot vas lancer le fichier correspondant présent dans le dossier `bot/src/jobs`.
Ce fichier est une liste d'action à faire sur Youtube.
Ces action sont décrite dans le fichier `bot/src/module/youtube/youtubeAction.ts`.

#### Navigation

Le fichier `bot/src/module/youtube/youtubeAction.ts` regroupe toutes les action de navigation possible que l'on appeler depuis les jobs.

Lors de la navigation des données seront récupérée via le fichier `bot/src/module/youtube/videoScrapper.ts`

#### Collecte des données

Le fichier `bot/src/module/youtube/videoScrapper.ts` regroupe toute les méthode récupérant les valeur des différents élément html de la page. Par exemple le titre des vidéos, leurs urls, la date...

Ces élément sont récupérée à l'aide de sélecteur CSS décris dans le fichier `bot/src/module/youtube/selectors.ts`

Les données extraites sont regroupé dans la classe `bot/src/module/youtube/video.ts` puis renvoyer sur la sortie standard pour être récupérées par cli.

### Traitement des données

Le traitement des données ce fais via Cli. Cli récupère sous format JSON les données de navigation et les transforme en csv avec la librairie pandas.

Cli permet aussi de déterminer pour chaque vidéo si cette même vidéo est disponible sur la plateforme YoutubeKids et la catégorie d'age pour laquelle elle est disponible.

### Schéma UML du Bot
![Alt text](./img/uml_bot.svg?raw=true "uml")
