import datetime
import os
import pickle
import re

from core.src.bot import runJob
from core.src.config import get_channel_base_name
from core.src.user_agent_generator import generate_user_agent_and_resolution

regex = re.compile(r'[\n\r\t]')


def get_or_load(chan, lang, cookie, always_get=False, export=True, fetch_modification_timestamp=None, meta_type=None):
    """
    Returns channel videos if exists, if not fetches them from online and saves it.
    :param fetch_modification_timestamp: to re-fetch channel videos, crontab timestamp parameter could be set to update downloaded files
    :param export: flag to control export
    :param always_get: whatever the videos are extracted before or not, always new videos are fetched
    :param chan: channel json object
    :param lang: which browser language will be used to access channel's homepage
    :param cookie: cookie if exists
    :param meta_type: to set meta type of the channels on meta experiments
    :return: channel videos
    """
    channel_file_name = get_channel_base_name(chan["channel"])

    fetch = False
    if not os.path.isfile(channel_file_name + ".pkl"):
        fetch = True
    elif always_get:
        fetch = True
    elif fetch_modification_timestamp:
        getmtime = os.path.getmtime(channel_file_name + ".pkl")
        fetch = datetime.datetime.now() - datetime.datetime.fromtimestamp(getmtime) > datetime.timedelta(
            hours=fetch_modification_timestamp)
    if fetch:
        events = [
            '{"type": "channelSniffer", "searchSelection": 0, "channel_id": "' + chan[
                "id"] + '", "searchTerm": "' + regex.sub(" ", chan["channel"]).replace("'",
                                                                                       "") + '", "getAll": true}',
        ]

        if meta_type and meta_type == "meta":
            events[0] = events[0][:-1] + ', "metaChannel":true}'
        elif meta_type and meta_type == "custom":
            events[0] = events[0][:-1] + ', "customYtChannel":true}'

        user_agent_resolution = generate_user_agent_and_resolution()
        try:
            data_json = runJob(events, user_agent_resolution, cookie, lang, None)
            data_json = [a for a in data_json if
                         "#shorts" not in a['title'].lower() and "live" not in a['title'].lower() and a[
                             'duration'] and ":" in a['duration'] and (
                                 len(a['duration'].split(":")) > 1 or int(
                             a['duration'].split(":")[
                                 -2]) < 1)]  # ignore videos less than 1 minute, live videos and #shorts
        except Exception as e:
            print("exception during channel sniffing, events: ", events)
            raise e

        if export and data_json and len(data_json) > 0:
            with open(channel_file_name + ".pkl", 'wb') as f:
                pickle.dump(data_json, f, protocol=4)
            with open(channel_file_name + ".txt", 'w') as f:
                f.write(str(data_json))
                f.close()
        return data_json
    else:
        with open(channel_file_name + ".pkl", 'rb') as f:
            return pickle.load(f)
