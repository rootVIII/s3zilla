# MIT License Copyright (c) 2019-2023 rootVIII
from os import listdir, path


def folder_walk(dir_path: str, contents: list) -> list:
    for file_name in listdir(dir_path):
        abs_path = path.join(dir_path, file_name)
        if path.isdir(abs_path):
            abs_path += '/'
            if abs_path not in contents:
                contents.append(abs_path)
                folder_walk(abs_path, contents)
        else:
            contents.append(abs_path)
    return contents
