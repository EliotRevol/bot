import json
import random

import pandas as pd


## @package user_agent_generator
#  Générateur aléatoire de user agent et de résolution
#

## Génère une résolution aléatoire
# @return Résolution json
from core.src import config
from core.src.config import USER_AGENT_CSV, INPUT_RESOLUTION_CSV


def generate_resolution():
    df = pd.read_csv(config.get_path(INPUT_RESOLUTION_CSV))
    resolution_list = json.loads(
        df.to_json(orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms",
                   default_handler=None))
    resolution = random.choice(resolution_list)
    return resolution


## Génère un user agent aléatoire
# @return UserAgent json
def generate_user_agent():
    df = pd.read_csv(config.get_path(USER_AGENT_CSV))
    user_agent_list = json.loads(
        df.to_json(orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms",
                   default_handler=None))
    user_agent = random.choice(user_agent_list)
    return user_agent


## Génère un user agent et une résolution aléatoire
# @return User agent & Résolution json
def generate_user_agent_and_resolution():
    user_agent = generate_user_agent()
    resolution = generate_resolution()
    return {'user_agent': user_agent['user_agent'], 'width': resolution['width'], 'height': resolution['height']}
