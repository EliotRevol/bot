import logging
import random
import re
import time
from abc import ABC

from core.src.bot import runJob
from core.src.channel_sniffer import get_or_load
from core.src.user_agent_generator import generate_user_agent_and_resolution
from experiments.base import Experiment

"""
Some codes in experiment regardless of election or generic are common. 
In order to prevent duplicated code some adapter classes are defined here. 
Experiments inherited from these adapter classes must be also inherits @ElectionExperiment or @GenericExperiment
"""


class WalkExperimentAdapter(Experiment, ABC):
    """
    Adapter class for welcome walk experiments, prevent duplicated code both for election and generic experiments.
    Aim is to combine two stage for walks:
    1) Initial startup point (event)
    2) Video watching
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.clean_space_regex = re.compile(r'[\n\r\t]')

    def run_walk(self, filename, initial_events):
        """
        Runs the initial startup events from container to choose random video from results, then makes walks
        :param filename: filename prefix to save results
        :param initial_events: startup container events for bot
        """
        data_json = runJob(initial_events, generate_user_agent_and_resolution(), self.cookie)
        if len(data_json) > 0:
            rvk = random.choice(data_json)
            self.walk_over_video(filename, rvk)
        else:
            logging.warning("no video are extracted from channel sniffing")

    def walk_over_video(self, filename, rvk):
        logging.info(f"Chosen video, url: {rvk['url']}, title: {rvk['title']}")
        video_id = rvk["url"].replace("https://www.youtube.com/watch?v=", "")
        video_title = self.clean_space_regex.sub(" ", rvk["title"])
        events = [
            '{"type": "fetch", "searchSelection":3}',
            '{"type": "watchOne", "video_id": "' + video_id + '", "searchTerm": "' + video_title + '", "watchTime": ' + str(
                self.watchTime) + ', "alea": ' + str(self.alea) + '}',
            '{"type": "fetchAutoplay", "searchSelection": ' + str(self.nb_walks) + ', "watchTime":  ' + str(
                self.watchTime) + ', "alea": ' + str(self.alea) + ' }',
            '{"type": "fetch", "searchSelection":3}'
        ]
        self.run_and_dump(events, filename)


def prepare_sniffing_event_for_meta(channel):
    if channel['meta-type'] == "meta":
        meta = "metaChannel"
    else:
        meta = "customYtChannel"
    events = [

        f'{{"type": "channelSniffer", "searchSelection": 0, "channel_id": "{channel["id"]}", '
        f'"searchTerm":"{channel["channel"]}", "getAll": true,"{meta}": true}}'
        ,
    ]
    return events


class ChannelPersonalizationAdapter(Experiment, ABC):
    """
     Adapter class for channel personalization walk experiments, prevent duplicated code both for election and generic experiments.
     Aim is to combine two stage for walks:
     1) Fill channels videos
     2) Video watching
     """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.channels = kwargs['channels']
        self.clean_space_regex = re.compile(r'[\n\r\t]')
        self.channel_sniffing_reload_hour = kwargs['channel_sniffing_reload_hour']

    def run_personalized_channel_walk(self, filename, starts):
        events = [
            '{"type": "fetch", "searchSelection":3}',
        ]

        for s in starts:
            events.append('{"type": "watchOne", "video_id": "' + s[
                "video_id"] + '", "searchTerm": "' + self.clean_space_regex.sub(" ",
                                                                                s[
                                                                                    "searchTerm"]) + '", "watchTime": ' + str(
                self.watchTime) + ', "alea": ' + str(self.alea) + '}')
            events.append('{"type": "fetch", "searchSelection":3}')
        self.run_and_dump(events, filename)

    def fill_and_run_personalized_channel_walk(self, filename, channel):

        events = prepare_sniffing_event_for_meta(channel)

        data_json = runJob(events, generate_user_agent_and_resolution(), self.cookie)
        if len(data_json) > 0:
            choices = random.choices(data_json, k=self.nb_walks)
            videos = [{"video_id": rvk["url"].replace("https://www.youtube.com/watch?v=", ""),
                       "searchTerm": self.clean_space_regex.sub(" ", rvk["title"]), "tag": channel} for rvk in
                      choices]
            self.run_personalized_channel_walk(filename, videos)
        else:
            logging.warning("no video are extracted from channel sniffing")
            time.sleep(100)

    def fill_channels_videos(self):
        logging.info("Populating videos in channels, number of channels: %d" % len(self.channels))
        channels_videos = {}
        channels_type = {}
        for chan in self.channels:
            meta_type = None
            if "meta-type" in chan:
                meta_type = chan['meta-type']
            channels_videos[chan["channel"]] = get_or_load(chan, self.lang, self.cookie,
                                                           fetch_modification_timestamp=self.channel_sniffing_reload_hour,
                                                           meta_type=meta_type)
            if "type" in chan:
                channels_type[chan["channel"]] = chan["type"]
            elif "meta-name" in chan:
                channels_type[chan["channel"]] = chan["meta-name"]
        return channels_videos, channels_type
