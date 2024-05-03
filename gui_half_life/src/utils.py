import gzip
import json
import time

import gensim
import regex


def get_timestamp():
    return str(time.time()).split('.')[0]

def check_with_accent(candidate_name, title):
    """
    Checks if name exist in a string. If cannot find it merges spaces then deaccent the name.
    :param candidate_name:
    :param title:
    :return:
    """
    if candidate_name in title:
        if candidate_name == "le pen":
            regex_str = candidate_name + r"[^a-zA-Z]"
            if len(regex.findall(regex_str, title)) > 0:
                return True
            else:
                return False
        elif candidate_name == "roussel":
            if "gaëtan" not in title:
                return True
            else:
                return False
        else:
            return True
    elif candidate_name.replace(" ", "") in title:
        return True
    elif gensim.utils.deaccent(candidate_name) in title:
        return True
    elif candidate_name.replace("-", " ") in title:
        return True
    else:
        return False


def multi_check_with_accent(candidate_list, title):
    """
    Checks if name exist in a string. If cannot find it merges spaces then deaccent the name.
    :param candidate_list:
    :param title:
    :return:
    """
    found = False
    for candidate_name in candidate_list:
        candidate_name = candidate_name.lower()
        if candidate_name != "":
            if candidate_name in title:
                if candidate_name in ["le pen", "rn", "lfi", "udc", "pcf", "eelv", "lr", "rec"]:
                    regex_str = r"[^a-zA-Z]" + candidate_name + r"[^a-zA-Z]"
                    if len(regex.findall(regex_str, title)) > 0:
                        found = True
                elif candidate_name == "roussel":
                    if "gaëtan" not in title:
                        found = True

                else:
                    found = True
            elif candidate_name.replace(" ", "") in title:
                found = True
            elif gensim.utils.deaccent(candidate_name) in title:
                found = True
            elif candidate_name.replace("-", " ") in title:
                found = True
        if found:
            return True
    return False


# return (candidate_name in title) or (
#         candidate_name.replace(" ", "") in title) or (
#                gensim.utils.deaccent(candidate_name) in title or candidate_name.replace("-", " ") in title)


def read_transcript(path):
    try:
        with gzip.open(path, "rt") as f:
            s = f.read()
        result = s.replace("\'", '"').replace('<Status.UNAVAILABLE: "Unavailable">', '"Unavailable"')
        return json.loads(result)
    except json.decoder.JSONDecodeError:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)


if __name__ == '__main__':
    test_str = ("M1 iPad Pro vs Galaxy Tab S7+ // Apple Pencil Writing")

    check_with_accent("Le Pen".lower(), test_str.lower())
