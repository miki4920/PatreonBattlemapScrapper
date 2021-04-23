import zipfile

from JsonHandler import write_submission_dictionary
from UtilityFunctions import read_json
from config import CONFIG
from os import walk, makedirs, path, listdir, remove
from shutil import move, rmtree, Error
import re


def get_submission_name(submission):
    file_name = submission["photos"][0]
    file_name = file_name.split("\\")[1].split("-")[0]
    file_name = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
    file_name = re.sub("(_)+", "_", file_name)
    file_name = re.sub("_$|^_", "", file_name)
    size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", file_name)
    width, height = "", ""
    if size:
        width, height = list(map(int, size.group(0).split("x")))
    return file_name, width, height


def extract_zip(zip_path):
    makedirs(CONFIG.map_path + "temp", exist_ok=True)
    directory = zipfile.ZipFile(zip_path)
    directory.extractall(CONFIG.map_path + "temp")


def get_images():
    images = []
    for r, d, f in walk(CONFIG.map_path + "temp"):
        for file in f:
            if file.endswith(".jpg") and not file.startswith("._"):
                images.append(path.join(r, file))
    for image in images:
        try:
            move(image, CONFIG.map_path + "temp")
        except Error:
            pass
    temp_path = listdir(CONFIG.map_path + "temp")
    for dir in temp_path:
        if path.isdir(CONFIG.map_path + "temp\\" + dir):
            rmtree(CONFIG.map_path + "temp\\" + dir)


def move_images(name):
    makedirs(CONFIG.map_path + name, exist_ok=True)
    temp_path = listdir(CONFIG.map_path + "temp")
    paths = []
    for file in temp_path:
        try:
            move(CONFIG.map_path + "temp\\" + file, CONFIG.map_path + name)
            paths.append(CONFIG.map_path + name + "\\" + file)
        except Error:
            pass
    rmtree(CONFIG.map_path + "temp")
    return paths


def delete_zip(zip_path):
    remove(zip_path)


def get_all_images():
    submission_list = read_json(CONFIG.dictionary_path)
    for i in range(0, len(submission_list)):
        if len(submission_list[i]["photos"]) > 0:
            name, width, height = get_submission_name(submission_list[i])
            submission_list[i]["name"] = name
            submission_list[i]["width"] = width
            submission_list[i]["height"] = height
            for file in submission_list[i]["photos"]:
                extract_zip(file)
                delete_zip(file)
            get_images()
            submission_list[i]["photos"] = move_images(name)
    write_submission_dictionary(submission_list)


get_all_images()
