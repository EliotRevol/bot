import glob
import gzip
import json
import os
import pickle

from utils.const import ResultTypes


def read_transcript(path):
    try:
        with gzip.open(path, "rt") as f:
            s = f.read()
        result = s.replace("\'", '"').replace('<Status.UNAVAILABLE: "Unavailable">', '"Unavailable"')
        return json.loads(result)
    except json.decoder.JSONDecodeError:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)


def read_json_gz(file_path):
    with gzip.open(file_path, "rt") as f:
        return eval(f.read())


def read_multi_folder(experiment_folder, experiment_type, result_type, data_folder="../../data"):
    files = []
    [files.extend(glob.glob(data_folder + "/*/" + f + "/*")) for f in experiment_folder]

    experiments_json = []
    if result_type == ResultTypes.TRANSCRIPT:
        [experiments_json.extend([a for a in read_transcript(f) if a['status'] == 'Status.OK']) for f in files if
         (result_type in f) and (experiment_type in f)]  # each transcript folder represents each experiment
    elif result_type == ResultTypes.HTML:
        [experiments_json.extend([a for a in read_json_gz(f)]) for f in files if
         (result_type in f) and (experiment_type in f)]  # each transcript folder represents each experiment
    elif result_type == ResultTypes.JSON:
        [experiments_json.append([a for a in read_json(f)]) for f in files if
         (result_type in f) and (experiment_type in f)]  # group each experiment json as one item inside list

    return experiments_json


def read_experiment_files(experiment_folder, experiment_type, result_type):
    print("Experiment folder: ", experiment_folder)
    print("Experiment type: ", experiment_type)
    print("Result type: ", result_type)
    if not experiment_folder.endswith("/"):
        experiment_folder += "/"
    files = glob.glob("*/" + experiment_folder + "*" + result_type)
    files = [f for f in files if experiment_type in f]
    print("Number of files: ", len(files))
    return files


def read_experiments(experiment_folder, experiment_type, result_type):
    files = read_experiment_files(experiment_folder, experiment_type, result_type)
    if result_type == ResultTypes.JSON:
        result = [read_json(f) for f in files]
    elif result_type == ResultTypes.TRANSCRIPT:
        result = [read_transcript(f) for f in files]
    else:
        raise NotImplementedError
    return result


def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def dump_pickle(file_path, obj):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, f)


def read_pickle(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)


def dump_json(file_path, obj):
    with open(file_path, "w") as f:
        json.dump(obj, f)
