import glob
import logging
import multiprocessing
import pickle
import random
import re

import numpy as np
import pandas as pd
import tqdm
from joblib import Parallel, delayed

from core.src.bot import runJob
from core.src.user_agent_generator import generate_user_agent_and_resolution
from core.src.youtube_api import get_randoms_videos
from core.src.ytkids import resolv
from experiments.adapter import WalkExperimentAdapter, ChannelPersonalizationAdapter
from experiments.base import GenericExperiment, ExperimentUnsetSettings


class WelcomeWalkExperiment(GenericExperiment, WalkExperimentAdapter):
    """
    Welcome walk generic experiment. @WelcomeWalkExperimentAdapter is used to run bot code.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            filename = "welcome-k"  "_" + str(self.nb_walks) + "_" + str(random.randint(1, 10000))
            logging.info(f"Welcome Experiment, iteration: {iteration:d} ,name: {filename}")
            events = [
                '{"type": "fetch", "searchSelection":1}',
            ]
            self.run_walk(filename, events)


class ResolveExperiment(GenericExperiment):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.resolve_regex = kwargs['resolve_regex']

    def resolve(self, id):
        return id, resolv(id)

    def run(self):
        video_list = glob.glob(self.resolve_regex)
        unique_urls = pd.concat([pd.read_csv(a)["url"] for a in video_list]).unique()
        with open("ytkids_urls.pkl", "rb") as f:
            load = pickle.load(f)
        # results = Parallel(n_jobs=multiprocessing.cpu_count())(
        #     delayed(self.resolve)(id) for id in tqdm.tqdm(unique_urls))
        # with open("ytkids_urls_17_02_2022.pkl", "wb") as f:
        #     pickle.dump(results, f)

        # unique_urlslist=unique_urls.tolist()
        # fetched_videos=[a[0] for a in load]
        # fetching_videos=set(unique_urlslist) - set(fetched_videos)
        # results = Parallel(n_jobs=multiprocessing.cpu_count())(
        #     delayed(self.resolve)(id) for id in tqdm.tqdm(fetching_videos))
        # with open("ytkids_urls_17_02_2022.pkl", "wb") as f:
        #     pickle.dump(results, f)

        with open("ytkids_urls_17_02_2022.pkl", "rb") as f:
            load.extend(pickle.load(f))
        url_ytkids_dict = {x: y for x, y in load}
        print(len(url_ytkids_dict))
        url_ytkids_dict[np.nan] = 'NA'
        for video in tqdm.tqdm(video_list):
            df = pd.read_csv(video)
            df['ytkids'] = df.url.map(lambda x: url_ytkids_dict[x])
            df.to_csv(video, index=None)

        # url_ytkids = dict.fromkeys(unique_urls)
        # logging.info(f"Populating {len(video_list):d} experiments")
        # for file in video_list:
        #     logging.info(f"Resolve: populating: {file}")
        #     populate_ytkids(file)
        # logging.info(f"Populated {len(video_list):d} experiments")


class ChannelWalkExperiment(GenericExperiment, WalkExperimentAdapter, ChannelPersonalizationAdapter):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']

    def run(self):

        channels_videos, channels_type = self.fill_channels_videos()
        iteration = 0
        while True:
            iteration += 1
            channel = random.choice(list(channels_videos))
            rvk = random.choice(channels_videos[channel])
            filename = "autoplay-k-" + channels_type[channel] + "-" + channel + "_" + str(self.nb_walks) + "_" + str(
                random.randint(1, 10000))
            self.walk_over_video(filename, rvk)

            logging.info(f"Number of runs: {iteration:d}, filename: {filename}")


class TestExperiment(GenericExperiment):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def run(self):
        self.events = [
            '{"type": "channelSniffer", "searchSelection": 0, "channel_id": "/user/HG13710", "searchTerm":"Gerard '
            'Heiries", "getAll": true}',
        ]
        data_json = runJob(self.events, generate_user_agent_and_resolution(), self.args['cookie'], self.lang,
                           self.save_html)

        for line in data_json:
            print(line['url'], line['title'], line['views'])


class ChannelPersonalizationExperiment(GenericExperiment, ChannelPersonalizationAdapter):
    """
    Personalization experiment.
    Aim is to fetch random channels from kids channels, playing their videos and fetching recommendations.
    As by watching videos more and more on the same content, personalized recommendations are expected.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']
        self.channel_sniffing_reload_hour = kwargs['channel_sniffing_reload_hour']

    def run(self):
        channels_videos, channels_type = self.fill_channels_videos()
        iteration = 0
        while True:
            iteration += 1
            channel = random.choice(list(channels_videos))
            logging.info(f"Chosen candidate: {channel}")
            random_videos_from_channel = random.choices(channels_videos[channel], k=self.nb_walks)

            start = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
                      "searchTerm": self.clean_space_regex.sub(" ", rvk["title"]), "tag": channel} for rvk in
                     random_videos_from_channel]
            filename = "autoplay-k-" + channels_type[channel] + "-" + channel + "_" + str(self.nb_walks) + "_" + str(
                random.randint(1, 10000))
            self.run_personalized_channel_walk(filename, start)
            logging.info(f"Number of runs: {iteration:d}, filename: {filename}")


class WelcomeWatchExperiment(GenericExperiment, ChannelPersonalizationAdapter):
    """
    Welcome watch experiment.
    Aim is to fetch random videos from welcome page, then watch and fetch welcome page
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def run(self):
        iteration = 0

        while True:
            iteration += 1

            events = [
                '{"type": "fetch", "searchSelection":1}',  # 1 time search is enough for choosing a video
            ]
            data_json = runJob(events, generate_user_agent_and_resolution(), self.cookie)
            logging.info(f"fetched videos, length: {len(data_json)}")
            if len(data_json) > self.nb_walks:
                selected_videos = random.choices(data_json, k=self.nb_walks)
                start = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
                          "searchTerm": self.clean_space_regex.sub(" ", rvk["title"])} for rvk in
                         selected_videos]
                filename = "autoplay-k-kids-random_" + str(self.nb_walks) + "_" + str(
                    random.randint(1, 10000))

                self.run_personalized_channel_walk(filename, start)
                logging.info(f"Number of runs: {iteration:d}, filename: {filename}")
