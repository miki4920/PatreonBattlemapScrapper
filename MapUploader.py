import requests
from requests_toolbelt import MultipartEncoder

from UtilityFunctions import read_json
from config import cfg


def upload_file_java():
    submission_list = read_json(cfg.dictionary_path)
    for submission in submission_list:
        for image in submission["photos"]:
            fields = [
                ('image', (submission["name"]+".jpg", open(image, 'rb'),
                           'image/jpg')),
                ('name', 'nick'),
            ]
            if submission["width"]:
                fields.extend([('squareWidth', submission["width"]),
                               ('squareHeight', submission["height"])])
            fields.extend([("tags", tag) for tag in submission["tags"]])
            multipart_data = MultipartEncoder(
                fields=fields
            )
            try:
                response = requests.post("http://192.168.0.40/api/images", data=multipart_data,
                                         headers={'Content-Type': multipart_data.content_type})
                print(response)
            except Exception as e:
                print(e)

upload_file_java()