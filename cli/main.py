import argparse
import os
from urllib.parse import unquote
import sys

sys.path.append("../")
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
from core.src.bot import runJob
from core.src.export import save_json, save_csv
from core.src.user_agent_generator import generate_user_agent_and_resolution

events = ['{"type": "watchOne", "video_id": "3mbpe-Jl3M", "searchTerm":"Raphaël Glucksmann : On fait la même erreur avec Xi Jinping qu avec Vladimir Poutine", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "LwNpZ9Lw7Yk", "searchTerm":" Le président chinois Xi Jinping en France : Il ne faut pas le traiter en ami", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "bqD5Z0IM4fs", "searchTerm":"La France est à la traîne sur l aide à l Ukraine : l interview en intégralité de Raphaël Glucksmann", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "JrakvQ9n5Ug", "searchTerm":"Raphaël Glucksmann : Le gouvernement Netanyahou n offre aucune perspective aux palestiniens", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "PX0BnQEPYD8", "searchTerm":"GLUCKSMANN CHAHUTÉ, MÉLENCHON ACCUSÉ : IL Y A T-IL « DEUX GAUCHES »IRRÉCONCILIABLES ?", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "LwNpZ9Lw7Yk", "searchTerm":"Le président chinois Xi Jinping en France : Il ne faut pas le traiter en ami. ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "OiLbOiHfW4I", "searchTerm":"GAZA, PARIS EST AVEC TOI : AU-DELÀ DE LA POLÉMIQUE GLUCKSMANN, LE VRAI VISAGE DU DÉFILÉ DU 1ER MAI ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "VI1HuzaPO2k", "searchTerm":"Raphaël Glucksmann, socialiste isolé en Europe - Patrick Cohen - C à vous - 02/05/2024 ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "mtyWEF0-XlE", "searchTerm":"R.Glucksmann répond à Tom Benoit en direct à propos de l’utilisation de l’épargne privée par l’UE ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "pLpa4JY9ovA", "searchTerm":"« Face aux Territoires » avec Raphaël Glucksmann ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "lj64t9DM7Jk", "searchTerm":"Bardella, Glucksmann : les visages souriants de l’anti-macronisme", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "Yz9R8BYMisY", "searchTerm":"« Européennes : bientôt Glucksmann devant Hayer ? ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "U0N_UNlqNHA", "searchTerm":" Sciences Po : Raphaël Glucksmann veut une évacuation des étudiants ! | Apolline Matin ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "CofiSxtWssA", "searchTerm":" Européennes : Raphaël Glucksmann talonne Valérie Hayer ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "AOQnq2ipNyg", "searchTerm":" Européennes : la percée Glucksmann - Reportage #cdanslair 16.04.2024 ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "yOnnJERoi7A", "searchTerm":" L échappée Bardella, la remontada Glucksmann - Reportage #cdanslair 16.04.2024 ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "_xzRSOBBp2U", "searchTerm":" Élections européennes - Raphaël Glucksmann est-il le candidat qui inquiète Emmanuel Macron ? ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "SjnXmmeQc-0", "searchTerm":" EUROPÉENNES : A QUOI SERT GLUCKSMANN ?", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "KEGEB2vRr80", "searchTerm":" Qui a peur de Raphaël Glucksmann ? ", "watchTime": 180000}',
          '{"type": "watchOne", "video_id": "3dTMbRAFW8M", "searchTerm":" Raphaël Glucksmann: Nous voulons apporter un grand plan de financement pour cette transition", "watchTime": 180000}',
          '{"type": "fetchAutoplay", "searchSelection": 85, "watchTime": 180000}',
          ]

out_path = './output/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="output filename")
    parser.add_argument("-c", "--cookie", help="cookies filename")
    args = parser.parse_args()
    ################################################
    # Launch with user agent and screen resolution #
    ################################################
    user_agent_resolution = generate_user_agent_and_resolution()
    res = runJob(events, user_agent_resolution, args.cookie)
    ###################################################
    # Launch without user agent and screen resolution #
    ###################################################
    # res = runJob(events,None,None,None)
    for elem in res:
        print(unquote(elem['title']))
    print(res)
    save_json(res, args.filename)
    save_csv(res, args.filename)
    # run_bot(events, out_path, args.filename)

    #################################
    # Get 4 random youtube video id #
    #################################
    # print(get_randoms_videos(4))
