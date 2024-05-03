import argparse
import os
from urllib.parse import unquote
import sys

sys.path.append("../")
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())
from core.src.bot import runJob
from core.src.export import save_json, save_csv
from core.src.user_agent_generator import generate_user_agent_and_resolution

events = ['{"type": "watchOne", "video_id": "bEbwmJy3xW8", "searchTerm":"Je vais à la mosquée pour la première fois", "watchTime": 6000}',
          '{"type": "fetchAutoplay", "searchSelection": 5, "watchTime": 6000}',
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
