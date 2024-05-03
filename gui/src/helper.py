import json
import random
import re

import regex
import requests
from scrapy.http import HtmlResponse


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def fetch_channel_name(url):
    """
    Fetches channel name from the given url
    :param url: Youtube video url
    :return: channel name
    """
    result = requests.get(url,
                          cookies={'CONSENT': 'YES+cb.20210328-17-p0.en-GB+FX+{}'.format(random.randint(100, 999))})
    response = HtmlResponse(url=url, body=result.content)
    json_raw = striphtml(response.css('script:contains(responseContext)').extract()[0])

    pattern = regex.compile(r"{(?:[^{}]*|(?R))*}")
    pattern.findall(json_raw)
    json_raw = next((x for x in pattern.findall(json_raw) if "responseContext" in x), None)
    if json_raw is None:
        channel_name = url.split("/")[-1]
    else:
        json_string = json.loads(json_raw)
        channel_name = json_string['metadata']['channelMetadataRenderer']['title']
    return channel_name
