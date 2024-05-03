# Known Bugs

## Sélecteur non trouver

![Alt text](./img/failed_to_find_selector.png?raw=true "failed_to_find_selector")

### Causes

Puppeteer n'a pas réussi a récupérer un élément dans la page html. L'élément a soit disparus soit a changé de nom.

### Solution

Dans l'erreur en screenchot le sélecteur qui pose problème est indiqué c'est : `"#video-title.style-scope.ytd-compact-video-renderer"`
Gardez cette valeur en tête.

Allez dans le fichier : `bot/src/module/youtube/selectors.ts`
Repérez la sélecteur qui pose problème: ici `VideoPage.__AUTOPLAY__TITLE`

Allez dans le fichier `bot/src/module/youtube/youtubeAction.ts` répérer `VideoPage.__AUTOPLAY__TITLE` et essayer de comprendre ce que le sélecteur récupère comme élément html. Par exemple ici il récupère le titre de la première suggestion lorsque l'on visionne une vidéo.

Ouvrez un navigateur et mettez vous dans le même cas de figure que le bot lorsque qu'il utilise le sélecteur qui pose problème ici lorsque l'on regarde un vidéo. Avec la console javascript trouver la nouvelle valeur du sélecteur(clique droit sur l'élément et copy css selector).
