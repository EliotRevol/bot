import logging
import random
import time

from experiments.adapter import WalkExperimentAdapter, ChannelPersonalizationAdapter
from experiments.base import ElectionExperiment, get_timestamp

NATIONAL_NEWS_CHANNEL_ID = "UCcE169gw8kJCzyCJZXb7DQw"  # national news channel ID


class WelcomeElectionExperiment(ElectionExperiment):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.waiting_seconds = kwargs["waiting_seconds"]

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()

            filename = f"election-welcome-fetch-{timestamp}"
            logging.info(f"Election welcome fetch Experiment, iteration: {iteration:d} ,name: {filename}")

            events = [
                '{"type": "fetch", "searchSelection":3}',
            ]

            self.run_and_dump(events, filename)
            time.sleep(self.waiting_seconds)


class WelcomeWalkElectionExperiment(ElectionExperiment, WalkExperimentAdapter):
    """
    Welcome walk for election, @WelcomeWalkExperimentAdapter is used to run bot.
    """

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()

            filename = "election-welcome-walk-k"  "_" + str(self.nb_walks) + "_" + timestamp
            logging.info(f" Welcome Walk Election Experiment, iteration: {iteration:d} ,name: {filename}")
            events = [
                '{"type": "fetch", "searchSelection":1}',
            ]
            self.run_walk(filename, events)


class NationalNewsFetchElectionExperiment(ElectionExperiment):
    """
    National news fetch election experiment
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.waiting_seconds = kwargs["waiting_seconds"]
        self.channel_name = NATIONAL_NEWS_CHANNEL_ID

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()

            filename = f"election-national-news-fetch-{timestamp}"
            logging.info(f"Election National News Experiment, iteration: {iteration:d} ,name: {filename}")

            events = [

                f'{{"type": "channelSniffer", "searchSelection": 0, "channel_id": "/channel/{self.channel_name}", '
                f'"searchTerm":"{self.channel_name}", "getAll": true,"customYtChannel": true}}',
                # customYtChannel parameter says bot that the channel is not a proper channel.
                # It's a Youtube-made channel, so different events and selectors will work on bot.
            ]

            self.run_and_dump(events, filename)
            time.sleep(self.waiting_seconds)


class NationalNewsWalkElectionExperiment(ElectionExperiment, WalkExperimentAdapter):
    """
    National News walk experiment. Bot is run by @WalkExperimentAdapter
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channel_name = NATIONAL_NEWS_CHANNEL_ID

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()

            filename = "election-national-news-walk-k"  "_" + str(self.nb_walks) + "_" + timestamp
            logging.info(f"Election National News Walk Experiment, iteration: {iteration:d} ,name: {filename}")
            events = [

                f'{{"type": "channelSniffer", "searchSelection": 0, "channel_id": "/channel/{self.channel_name}", '
                f'"searchTerm":"{self.channel_name}", "getAll": true,"customYtChannel": true}}'
                ,
            ]
            self.run_walk(filename, events)


class ChannelPersonalizationElectionExperiment(ElectionExperiment, ChannelPersonalizationAdapter):
    """
    Channel Personalization walk experiment.
    Aim is to fetch random channels from candidates channels, playing their videos and fetching recommendations.
    As by watching videos more and more on the same content, personalized recommendations are expected.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']

    def run(self):

        channels_videos, _ = self.fill_channels_videos()
        iteration = 0
        while True:
            iteration += 1
            channel = random.choice(list(channels_videos))
            logging.info(f"Chosen candidate: {channel}")
            random_videos_from_channel = random.choices(channels_videos[channel], k=self.nb_walks)
            timestamp = get_timestamp()

            start = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
                      "searchTerm": self.clean_space_regex.sub(" ", rvk["title"]), "tag": channel} for rvk in
                     random_videos_from_channel]
            filename = "election-channel-personalization"  "_" + str(self.nb_walks) + "_" + timestamp
            self.run_personalized_channel_walk(filename, start)
            logging.info(f"Number of runs: {iteration:d}, filename: {filename}")
