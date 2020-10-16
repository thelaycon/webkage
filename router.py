# Router package for matching routes
import re


def path_to_regex(path):
    path_segments = path.split("/")
    params = dict()
    for index, segment in enumerate(path_segments):
        if segment == ":id":
            path_segments[index] = "[0-9]+"
        elif segment == ":slug":
            path_segments[index] = "[a-zA-Z]+(?:-[a-zA-Z]+)*"
    path = "/".join(path_segments) + "$"
    return path



def match_route(routes, path):
    for route in routes:
        match = re.match(route, path)
        if match is not None:
            return route


def get_params(match, path):
    path_segments = path.split("/")
    match_segments = match.split("/")
    id_ = None
    slug = None
    id_index = None
    slug_index = None
    if "[0-9]+" in match_segments:
        id_index = match_segments.index("[0-9]+")
    if "[a-zA-Z]+(?:-[a-zA-Z]+)*" in match_segments:
        slug_index = match_segments.index("[a-zA-Z]+(?:-[a-zA-Z]+)*")
    if id_index != None:
        id_ = path_segments[id_index]
    if slug_index != None:
        slug = path_segments[slug_index]

    return (id_, slug)






        
        





