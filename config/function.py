def set_classes(dictionary: dict, key: str,  new_values: tuple) -> tuple:
    classes = list(dictionary[key])
    for value in new_values:
        if not value in classes:
            classes.append(value)

    return tuple(classes)
