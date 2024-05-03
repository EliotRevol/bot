# coding: utf-8

import argparse
import glob
import os
import random as rd
import re
import sys

sys.path.append("../")
from core.src import config
from core.src.bot import runJob
from core.src.channel_sniffer import get_or_load
from core.src.user_agent_generator import generate_user_agent_and_resolution
from core.src.utils import dump
from core.src.youtube_api import get_randoms_videos
from core.src.ytkids import populate_ytkids

os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="output filename")
    parser.add_argument("-c", "--cookie", help="cookies filename")
    parser.add_argument("--save_html", help="save html of videos", action="store_true")
    # parser.add_argument("--save_transcripts", help="save transcripts of videos", action="store_true")
    parser.add_argument("--transcript_language", help="languages of the transcripts to fetch", nargs='+', default=[])
    parser.add_argument("--lang", help="language for the http headers and browser", default="en")
    parser.add_argument("--nb_runs", help="Number of runs", default=1000, type=int)
    parser.add_argument("--k", "--nb_walks", help="Number of walks", default=5, type=int)
    parser.add_argument("--watch_time", help="Watch Time of the videos", default=50000, type=int)
    parser.add_argument("--store_folder", help="Folder path to store experiment results", default=None)
    args = parser.parse_args()

    ''' what to run '''
    expes = ["welcome"]  # ,"rd"    # expe0 , resolve , walks , welcome
    # expes=["walks"]
    # naming = ["welcome"] #["expe2"]
    naming = ["expe2"]

    ''' globals '''
    k = args.k
    nb_runs = args.nb_runs
    watchTime = args.watch_time
    alea = int(watchTime / 10)

    lang = args.lang
    regex = re.compile(r'[\n\r\t]')
    # populating base channels cf Table 1 in https://arxiv.org/pdf/1908.08313.pdf (top-5 still available per type
    # kids: https://www.statista.com/statistics/785626/most-popular-youtube-children-channels-ranked-by-subscribers/
    channels = [
        {"channel": "Black Pigeon Speaks", "id": "/user/TokyoAtomic", "type": "AR"},  # alt right
        {"channel": "The Golden One", "id": "/user/TheLatsbrah", "type": "AR"},  # alt right
        {"channel": "NeatoBurrito Productions", "id": "/channel/UCZtDKD0pFpPclXA7ZAti90w", "type": "AR"},  # alt right
        {"channel": "Australian Realist ", "id": "/user/AustralianRealist", "type": "AR"},  # alt right
        {"channel": "Prince of Zimbabwe", "id": "/c/PrinceofZimbabwe", "type": "AR"},  # alt right
        {"channel": "Vox", "id": "/user/voxdotcom", "type": "media"},  # media
        {"channel": "GQ", "id": "/c/GQ", "type": "media"},  # media
        {"channel": "VICE News", "id": "/c/VICENews", "type": "media"},  # media
        {"channel": "WIRED", "id": "/user/wired", "type": "media"},  # media
        {"channel": "Vanity Fair", "id": "/c/VanityFair", "type": "media"},  # media
        {"channel": "PowerfulJRE", "id": "/user/PowerfulJRE", "type": "IDW"},
        {"channel": "JRE Clips", "id": "/c/JREClips", "type": "IDW"},
        {"channel": "PragerU", "id": "/user/PragerUniversity", "type": "IDW"},
        {"channel": "The Daily Wire", "id": "/c/TheDailyWire/", "type": "IDW"},
        {"channel": "The Rubin Report", "id": "/user/RubinReport", "type": "IDW"},
        {"channel": "StevenCrowder", "id": "/user/StevenCrowder", "type": "AL"},
        {"channel": "Rebel News", "id": "/c/RebelMediaTV", "type": "AL"},
        {"channel": "Paul Joseph Watson", "id": "/user/PrisonPlanetLive", "type": "AL"},
        {"channel": "Mark Dice", "id": "/user/MarkDice", "type": "AL"},
        {"channel": "Sargon of Akkad", "id": "/user/SargonofAkkad100", "type": "AL"},

        #                     {"channel": "Peppa Pig Français - Chaîne Officielle", "id": "c/PeppaPigFR", "type": "kids"},

        # {"channel": "ChuChu TV Nursery Rhymes & Kids Songs", "id": "/c/ChuChuTV", "type": "kids"},
        # {"channel": "El Reino Infantil", "id": "/c/elreinoinfantil", "type": "kids"},
        # {"channel": "Little Baby Bum - Nursery Rhymes & Kids Songs", "id": "/user/LittleBabyBum", "type": "kids"},
        # {"channel": "Masha and The Bear", "id": "/c/MashaBearEN", "type": "kids"},
        # {"channel": "Ryan s World", "id": "/c/RyanToysReview", "type": "kids"},
    ]  # {"channel": "", "id": "", "type": ""},

    # channels=[{"channel":,"id":"/channel/UCOPCqt3TWsBO0H1u-_Lw9CQ",type:""}]
    if "expe0" in expes:
        ''' Testing
        '''
        exp_name = "test-"

        args.filename = exp_name + str(rd.randint(1, 10000))

        events = [
            '{"type": "channelSniffer", "searchSelection": 0, "channel_id": "/user/HG13710", "searchTerm":"Gerard Heiries", "getAll": true}',
        ]

        user_agent_resolution = generate_user_agent_and_resolution()
        data_json = runJob(events, user_agent_resolution, args.cookie, lang, args.save_html)

        for line in data_json:
            print(line['url'], line['title'], line['views'])

    if "resolve" in expes:
        for file in glob.glob(
                config.get_output_dir() + "*20*.csv"):  # for file in glob.glob(out_path + "*_20_*.csv"):
            print("_ populating: " + file)
            populate_ytkids(file)

    if "walks" in expes:

        # populating videos in channels, long !
        channels_videos = {}
        channels_type = {}
        for chan in channels:
            channels_videos[chan["channel"]] = get_or_load(chan, lang, args.cookie)
            channels_type[chan["channel"]] = chan["type"]
        # print(channels_videos)

        #         while True: # stdev
        for i in range(nb_runs):
            channel = rd.choice(list(channels_videos))
            rvk = rd.choice(channels_videos[channel])

            starts = [
                {"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
                 "searchTerm": regex.sub(" ", rvk["title"]), "tag": channel},
            ]
            if "rd" in expes:
                rv = get_randoms_videos(1)  # for the random start point
                starts.append({"video_id": rv[0]['id'], "searchTerm": regex.sub(" ", rv[0]['title']), "tag": "random"})

            for s in starts:
                # crade
                if "expe1" in naming:
                    args.filename = "autoplay-k-" + channels_type[channel] + "-" + s["tag"] + "_" + str(k) + "_" + str(
                        rd.randint(1, 10000))
                elif "expe2" in naming:
                    args.filename = "proximity-" + channels_type[channel] + "-" + s["tag"] + "_" + str(k) + "_" + str(
                        rd.randint(1, 10000))
                else:
                    assert False
                print(args.filename)

                events = [
                    '{"type": "fetch", "searchSelection":3}',  # remove from gi alea 5 seconds
                    '{"type": "watchOne", "video_id": "' + s["video_id"] + '", "searchTerm": "' + regex.sub(" ", s[
                        "searchTerm"]) + '", "watchTime": ' + str(watchTime) + ', "alea": ' + str(alea) + '}',
                    '{"type": "fetchAutoplay", "searchSelection": ' + str(k) + ', "watchTime":  ' + str(alea) + ' }',
                    '{"type": "fetch", "searchSelection":3}'
                ]

                user_agent_resolution = generate_user_agent_and_resolution()

                result = runJob(events, user_agent_resolution, args.cookie, lang, args.save_html)
                dump(globals(), result, args.filename, args.save_html, args.cookie, args.transcript_language)

    if "welcome" in expes:

        while True:  # stdev

            args.filename = "welcome-k"  "_" + str(k) + "_" + str(rd.randint(1, 10000))
            print(args.filename)

            events = [
                '{"type": "fetch", "searchSelection":1}',
            ]

            user_agent_resolution = generate_user_agent_and_resolution()
            data_json = runJob(events, user_agent_resolution, args.cookie)

            rvk = rd.choice(data_json)
            print(rvk['url'], rvk['title'])

            events = [
                '{"type": "fetch", "searchSelection":3}',
                '{"type": "watchOne", "video_id": "' + rvk["url"].replace("https://www.youtube.com/watch?v=",
                                                                          "") + '", "searchTerm": "' + regex.sub(" ",
                                                                                                                 rvk[
                                                                                                                     "title"]) + '", "watchTime": ' + str(
                    watchTime) + ', "alea": ' + str(alea) + '}',
                '{"type": "fetchAutoplay", "searchSelection": ' + str(k) + ', "watchTime":  ' + str(alea) + ' }',
                '{"type": "fetch", "searchSelection":3}'
            ]

            result = runJob(events, user_agent_resolution, args.cookie, lang, args.save_html)
            dump(globals(), result, args.filename, args.save_html, args.cookie, args.transcript_language)
