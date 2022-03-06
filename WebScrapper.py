import concurrent.futures
from io import BytesIO
import os
import re
import requests

from zipfile import ZipFile

from config import CONFIG


class WebScrapper(object):
    def __init__(self):
        self.url = CONFIG.STARTING_URL
        self.create_directory()

    @staticmethod
    def create_directory():
        if not os.path.exists(CONFIG.MAP_PATH):
            os.makedirs(CONFIG.MAP_PATH)

    @staticmethod
    def download(url):
        download = requests.get(url, cookies=CONFIG.COOKIES)
        with ZipFile(BytesIO(download.content)) as download_zip:
            for name in download_zip.namelist():
                if re.match("^(?!__MACOSX).+GL_.+\.((jpg)|(png))", name):
                    path = re.search("GL_([\w\.]+)", name).group(1)
                    path = "".join(path.split("_"))
                    path = re.split("([A-Z][a-z]+)", path)
                    path = [word for word in path if len(word) >= 3]
                    path = CONFIG.MAP_PATH + "_".join(path[:-1]) + path[-1]
                    with open(path, "wb") as file:
                        file.write(download_zip.read(name))

    def scrape(self):
        while self.url:
            request = requests.get(self.url, cookies=CONFIG.COOKIES).text
            links = re.findall(CONFIG.LINK_REGEX, request)
            links = [link.replace("amp;", "") for link in links]
            with concurrent.futures.ThreadPoolExecutor() as exector:
                exector.map(self.download, links)
            self.url = re.search("\"next\":\"(https:\/\/[\w:\/\.\?=%&-]+)", request)
            self.url = self.url.group(1) if self.url else None


webscrapper = WebScrapper()
webscrapper.scrape()


