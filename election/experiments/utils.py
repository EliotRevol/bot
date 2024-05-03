import gensim
import regex


def find_candidate(title, candidate_list):
    author_str, title_str, tags_str = title
    found_candidates = []
    for candidate in candidate_list:
        candidate_lower = candidate.lower()
        if check_with_accent(candidate_lower, author_str):
            found_candidates.append(candidate)
            break  # definitive candidate, only one candidate -> author
        elif check_with_accent(candidate_lower, tags_str):
            found_candidates.append(candidate)
        elif check_with_accent(candidate_lower, title_str):
            found_candidates.append(candidate)
    if len(found_candidates) == 0:
        return [None]
    else:
        return found_candidates


def check_with_accent(candidate_name, title):
    """
    Checks if name exist in a string. If cannot find it merges spaces then deaccent the name.
    :param candidate_name:
    :param title:
    :return:
    """
    return (candidate_name in title) or (
            candidate_name.replace(" ", "") in title) or (
                   gensim.utils.deaccent(candidate_name) in title or candidate_name.replace("-", " ") in title)


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
                if candidate_name in ["le pen", "rn", "lfi", "udc", "pcf", "eelv", "lr", "rec", "tdp", "prv", "ps",
                                      "g.s", "lnd", "gé", "udi", "lc"]:
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
            elif candidate_name!="gé" and gensim.utils.deaccent(candidate_name) in title:
                found = True
            elif candidate_name.replace("-", " ") in title:
                found = True
        if found:
            return True
    return False


def include_keys(dictionary, keys):
    """Filters a dict by only including certain keys."""
    key_set = set(keys) & set(dictionary.keys())
    return {key: dictionary[key] for key in key_set}


def combine_candidate_clues(title, author, tags):
    title_str = ""
    author_str = ""
    tags_str = ""

    if len(tags) > 0:
        tags_str = "".join(tags).lower()
    if title:
        title_str = title.lower()
    if author:
        author_str = author.lower()
    return author_str, title_str, tags_str
