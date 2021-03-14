from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
import browser_cookie3 as cookies
from JsonHandler import *
from Submission import create_submission
from UtilityFunctions import *
from config import cfg


class WebScrapper(object):
    def __init__(self):
        self.cookies = eval(cfg.cookies)
        self.starting_url = cfg.starting_url
        self.submission_list = []
        if os.path.exists(cfg.dictionary_path):
            self.submission_list = read_json(cfg.dictionary_path)

    def get_request(self, url, stream=False):
        return requests.get(url, cookies=self.cookies, stream=stream)

    def get_submissions(self):
        request = self.get_request(self.starting_url).json()
        while True:
            for submission in request["data"]:
                links = get_download_links(submission)
                if links:
                    tags = get_user_tags(submission)
                    submission = create_submission(links, tags)
                    self.submission_list.append(submission)
            write_submission_dictionary(self.submission_list)
            next_url = get_next_url(request)
            if not next_url:
                break
            request = self.get_request(next_url).json()

    def download_file(self, submission):
        name_list = []
        for link in submission["links"]:
            request = self.get_request(link, stream=True)
            name = str(request.headers['content-disposition']).split("; ")[1]
            name = name.replace("filename=", "").strip("\"")
            name = cfg.map_path + name
            name_list.append(name)
            with open(name, "wb") as file:
                for data in request.iter_content(chunk_size=4096):
                    file.write(data)
        return submission, name_list

    def download_files(self):
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for submission in self.submission_list:
                future = executor.submit(self.download_file, submission)
                futures.append(future)
        futures, _ = concurrent.futures.wait(futures)
        for future in futures:
            try:
                submission, name_list = future.result()
                submission["compressed_photos"].extend(name_list)
            except Exception as e:
                print(e)
        write_submission_dictionary(self.submission_list)


webscrapper = WebScrapper()
webscrapper.get_submissions()
webscrapper.download_files()

