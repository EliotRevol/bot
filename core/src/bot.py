import json
import subprocess
import tempfile

from core.src import config


## @package bot
#  Module d'interaction avec le bot

## Lancement du bot.
# @param events JSON list
# @param userAgent string
# @param width résolution de l'écran
# @param height résolution de l'écran
# @param cookies nom du fichier de cookie
# @param lang langage du navigateur (en,fr,es,de...)
# @return Vidéo JSON list
def runJob(events, userAgentResoluton, cookies, lang=None, save_html=None):
    user_agent = userAgentResoluton['user_agent']
    width = userAgentResoluton['width']
    height = userAgentResoluton['height']
    events_string = "\'" + "\' \'".join(events) + "\'"
    args = '-e ' + events_string
    if width and height:
        args = args + ' -wr ' + str(width)
        args = args + ' -hr ' + str(height)
    if user_agent:
        args = args + " -u \'" + str(user_agent) + "\'"
    if cookies:
        args = args + " -c " + str(cookies)
    if lang:
        args = args + " -l " + str(lang)
    if save_html:
        args = args + " --save_html"

    pwd_cookies = config.get_cookies()
    if cookies:
        command = "docker container run -v " + pwd_cookies + ":/home/node/app/input bot " + args
    else:
        command = "docker container run bot " + args
    print(command)

    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as file:  # save docker output to temp file,
        subprocess.check_call(command, stdout=file, shell=True)
        file.seek(0)  # sync. with disk
        read = file.read()  # receive bot output
        print("----------------------------------")
        print(read)
    try:
        output = json.loads('[' + str(read)[:-2] + ']')
    except:
        print("exception")
        output = []
    return output
