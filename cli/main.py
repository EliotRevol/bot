import argparse
import os
from urllib.parse import unquote
import sys

sys.path.append("../")
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
from core.src.bot import runJob
from core.src.export import save_json, save_csv
from core.src.user_agent_generator import generate_user_agent_and_resolution

events = ['{"type": "watchOne", "video_id": "HR_UZhz9dwQ", "searchTerm":"Européennes: Bardella a-t-il tué le match ?", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "oQpryKlWYjY", "searchTerm":"Débat G. Attal / J. Bardella - Replay du 20H de TF1", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "OY2WvPg35-Y", "searchTerm":"Européennes: le premier débat entre Jordan Bardella et Valérie Hayer en intégralité", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "TmIVC9AGTuo", "searchTerm":"Jordan Bardella : L Europe doit mettre fin à une forme de naïveté à l égard de la mondialisation", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "OrPBJyDvp2w", "searchTerm":"L union fait la France !", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "VjILoreoNco", "searchTerm":"Jordan Bardella IMPLACABLE sur l insécurité ! | Apolline Matin", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "qJ_J4UcECiw", "searchTerm":"🔴 EN DIRECT - Jordan Bardella face aux Grandes Gueules !", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "70_vcb0EQtk", "searchTerm":"🔴 DIRECT - L intégrale de l interview de Jordan Bardella, président du RN, sur RMC", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "oOdXYFGohf0", "searchTerm":"Jordan Bardella répond à Eric Dupond-Moretti sur le tacle à Marine Le Pen !", "watchTime": 6000}',
          '{"type": "watchOne", "video_id": "mw4L2xmEtS8", "searchTerm":"Jordan Bardella face à Pascal Praud : Drame de Crépol, traitement médiatique, vie privée...", "watchTime": 6000}',
          '{"type": "fetchAutoplay", "searchSelection": 150, "watchTime": 6000}',
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
