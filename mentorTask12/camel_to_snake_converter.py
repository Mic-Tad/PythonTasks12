import re


def change_case(str):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(str):
    temp = str.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])
