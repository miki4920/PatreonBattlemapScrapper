import re
import json as j
from config import cfg


def get_download_links(json):
    try:
        content = json["attributes"]["content"]
        links = re.findall(cfg.regex_string, content)
        links = [link.replace("amp;", "") for link in links]
        return links
    except KeyError:
        return None


def get_user_tags(json):
    try:
        tag_list = []
        content = json["relationships"]["user_defined_tags"]["data"]
        for tag in content:
            tag = tag["id"].replace("user_defined;", "")
            tag_list.append(tag),
        return tag_list
    except KeyError:
        return None


def get_next_url(json):
    try:
        next_url = json["links"]["next"]
        return next_url
    except KeyError:
        return None


def write_submission_dictionary(submission_list):
    with open(cfg.dictionary_path, 'w') as file:
        j.dump(submission_list, file, indent=4)
