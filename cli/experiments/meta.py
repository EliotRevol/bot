import logging
import random

from experiments.adapter import ChannelPersonalizationAdapter, WalkExperimentAdapter, prepare_sniffing_event_for_meta
from experiments.base import get_timestamp


class MetaChannelPersonalization(ChannelPersonalizationAdapter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()
            channel = random.choice(self.channels)
            filename = "meta-channel-personalization_" + channel['meta-name'] + "_" + str(
                self.nb_walks) + "_" + timestamp
            logging.info(f"Chosen meta channel: {channel['channel']}, {channel['meta-name']}")

            self.fill_and_run_personalized_channel_walk(filename, channel)
            logging.info(f"Number of runs: {iteration:d}, filename: {filename}")


class MetaWalk(WalkExperimentAdapter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']

    def run(self):
        iteration = 0
        while True:
            iteration += 1
            timestamp = get_timestamp()
            channel = random.choice(self.channels)
            filename = "meta-walk_" + channel['meta-name'] + "_" + str(
                self.nb_walks) + "_" + timestamp
            logging.info(f"Chosen meta channel: {channel['channel']}, {channel['meta-name']}")

            events = prepare_sniffing_event_for_meta(channel)

            self.run_walk(filename, events)
            logging.info(f"Number of runs: {iteration:d}, filename: {filename}")
