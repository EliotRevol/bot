# coding: utf-8

import argparse
import json
import logging
import os
import sys

sys.path.append("../")
from experiments.factory import ElectionExperimentFactory, GenericExperimentFactory, MetaExperimentFactory
from core.src.utils import read_json

logging.basicConfig(level=logging.INFO)
os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="output filename")
    parser.add_argument("-c", "--cookie", help="cookies filename")
    parser.add_argument("--config", help="Config file for the experiment")

    # Parameters which can be also supplied from config json, see --config
    parameters = parser.add_argument_group("parameters")
    parameters.add_argument("--experiment", help="Experiment type")
    parameters.add_argument("--naming", help="Naming for storing experiment results")
    parameters.add_argument("--save_html", help="save html of videos", action="store_true")
    parameters.add_argument("--transcript_language", help="languages of the transcripts to fetch", nargs='+',
                            default=[])
    parameters.add_argument("--lang", help="language for the http headers and browser", default="en")
    parameters.add_argument("--nb_runs", help="Number of runs", default=1000, type=int)
    parameters.add_argument("--k", "--nb_walks", help="Number of walks", default=5, type=int)
    parameters.add_argument("--watch_time", help="Watch Time of the videos", default=50000, type=int)
    parameters.add_argument("--store_folder", help="Folder path to store experiment results", default=None)
    parameters.add_argument("--resolve_regex",
                            help="Regex pattern to select files in resolve, requires only in resolve experiment")
    parameters.add_argument("--random_start",
                            help="Random start flag during walks", action="store_true")
    parameters.add_argument("--alea",
                            help="Deviation +- from watch time as milliseconds", type=int)
    args = parser.parse_args()

    # If config json is supplied, all parameters will be updated from json file.
    if args.config is not None:
        logging.info(
            "Config path has been supplied to arguments")
        logging.info("Parameters from shell will be override parameters in config file.")
        with open(args.config, "r") as f:
            config_json = json.load(f)
        t_args = argparse.Namespace()
        t_args.__dict__.update(config_json)
        args = parser.parse_args(namespace=t_args)
    else:
        logging.info("No config has been supplied, using parameters from shell.")

    # if channels supplied as json path, read json file. Otherwise, it should be a json array
    if args.channels.endswith(".json"):
        args.channels = read_json(args.channels)
        logging.info("")
    return args


if __name__ == '__main__':
    args = parse_args()

    if "election" in args.experiment:
        experiment = ElectionExperimentFactory().create_experiment(**vars(args))
    elif "meta" in args.experiment:
        experiment = MetaExperimentFactory().create_experiment(**vars(args))
    else:
        experiment = GenericExperimentFactory().create_experiment(**vars(args))

    experiment.run()
