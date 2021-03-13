import os
import re


def get_download_links(json):
    try:
        content = json["attributes"]["content"]
        links = re.findall(r"<a href=\"(https:\/\/www\.patreon\.com\/file\?h=[0-9]+&amp;i=[0-9]+)\">[\w -]*\$5 Rewards", content)
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
        next_url = json["links"]
        return next_url
    except KeyError:
        return None
