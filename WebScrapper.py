import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import browser_cookie3 as cookies
from config import config
from JsonHandler import *
from UtilityFunctions import *
from Submission import Submission


class WebScrapper(object):
    def __init__(self):
        self.cookies = eval(config.cookies)
        self.starting_url = config.starting_url
        self.submission_list = []
        if os.path.exists(config.dictionary_path):
            self.submission_list = read_json(config.dictionary_path)

    def get_request(self, url, stream=False):
        return requests.get(url, cookies=self.cookies, stream=stream)

    def get_submissions(self):
        request = self.get_request(self.starting_url).json()
        while True:
            for submission in request["data"]:
                links = get_download_links(submission)
                if links:
                    tags = get_user_tags(submission)
                    submission = Submission(links, tags)
                    self.submission_list.append(submission)
            next_url = get_next_url(request)
            if not next_url:
                break
            request = self.get_request(next_url).json()

    def download_file(self, url):
        request = self.get_request(url, stream=True)
        name = re.search(r"filename=\"([\w \[\]\-\$\.]*)\";", request.headers['content-disposition']).group(1)
        with open("maps/" + name, "wb") as file:
            for data in request.iter_content(chunk_size=4096):
                file.write(data)







    # processes = []
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     for url in download_file_list:
    #         processes.append(executor.submit(download_file, url))
