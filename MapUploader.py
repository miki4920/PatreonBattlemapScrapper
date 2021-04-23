import requests
from requests_toolbelt import MultipartEncoder

from UtilityFunctions import read_json
from config import CONFIG


def upload_file_java():
    submission_list = read_json(CONFIG.dictionary_path)
    for submission in submission_list:
        if len(submission["tags"]) > 1:
            submission["tags"] = ",".join(submission["tags"])
        for image in submission["photos"]:
            image = {"picture": open(image, "rb")}

            metadata = {"name": submission["name"],
                        "extension": "jpg",
                        "uploader": "czepeku",
                        "square_width": submission["width"],
                        "square_height": submission["height"],
                        "tags": submission["tags"],
                        "ignore_hash": "true",
                        }
            try:
                response = requests.post("http://192.168.0.11:8000/maps/", data=metadata,
                                         files=image)
                print(response.content)
            except Exception as e:
                print(e)

upload_file_java()