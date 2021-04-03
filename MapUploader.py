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
                ('name', 'czepeku'),
            ]
            if submission["width"]:
                fields.extend([('squareWidth', submission["width"]),
                               ('squareHeight', submission["height"])])
            tags = [("tags", tag) for tag in submission["tags"]]
            if image.split("\\")[-1].startswith("GL"):
                tags.append(("tags", "nogrid"))
            else:
                tags.append(("tags", "grid"))
            fields.extend(tags)
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