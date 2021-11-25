import os

def set_classes(dictionary: dict, key: str,  new_values: tuple) -> tuple:
    classes = list(dictionary[key])
    for value in new_values:
        if not value in classes:
            classes.append(value)

    return tuple(classes)

def addbs(dir_path=None) -> str:
    new_path = None
    sep_path = os.path.sep

    if isinstance(dir_path, (str,)):
        if not dir_path.endswith(sep_path):
            new_path = dir_path + sep_path
    return new_path
