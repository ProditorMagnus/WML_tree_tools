#!/usr/bin/env python3
# encoding: utf-8

import pickle
from os.path import join, isfile
from collections import deque
import wmlparser3

#		 01234567
mode = 0b01001000  # program settings


# 0: show debug
# 1: show real
# 2: show extra
# 3: not used
# 4: cache
# 5: check performance

# takes more room this way, consider putting them to separate variables
def debug():
    return mode & 0b10000000


def prod():
    return mode & 0b01000000


def extra():
    return mode & 0b00100000


def _reserved_mode_():
    return mode & 0b00010000


def cache():
    return mode & 0b00001000


def perf():
    return mode & 0b00000100


if not cache():
    from subprocess import call

    call(["python", "preprocess_addon.py"])
    main = wmlparser3.Parser()
    root_node = main.parse_file(join("..", "preprocessed_addon", "_main.cfg"))
else:
    if isfile("node_cache.pickle"):
        with open("node_cache.pickle", "rb") as f:
            root_node = pickle.load(f)
    else:
        main = wmlparser3.Parser()
        root_node = main.parse_file(join("..", "preprocessed_addon", "_main.cfg"))
        with open("node_cache.pickle", "wb") as f:
            pickle.dump(root_node, f)


def query_matches(node, path, query):
    if path_invalidates_match(path, query[0], True):
        return False
    attr_query = query[1]
    if attr_query is not None:
        if node.get_name() != attr_query[0]:
            return False
        # TODO support other operators to compare, also ranges or lists
        attr_value = node.get_text()
        attr_wanted = attr_query[1]
        if attr_value is not None and attr_wanted == "*":
            return True
        else:
            if extra():
                print("attr check not finished")
                print("got", attr_value, "wanted", attr_wanted)
                input()
            if attr_value != attr_wanted:
                # print("got",attr_value, "wanted", attr_wanted)
                return False

    return True


def path_invalidates_match(path, query_path, return_exact=False):
    path = [n.get_name() for n in path]
    # if there is no way that this path can match query, with return_exact it checks that path is full match

    if extra(): print("inside path_invalidates_match", path, query_path)

    wanted = deque(query_path)
    actual = deque(path)

    star_open = False
    while len(wanted) > 0 and len(actual) > 0:
        # if
        w = wanted[0]
        a = actual[0]
        if w == "*":
            if extra(): print("star opened")
            star_open = True
            wanted.popleft()
            continue
        if a == w or w == "?":
            if extra(): print("a is w", a, w)
            wanted.popleft()
            actual.popleft()
            star_open = False
            continue
        if star_open:
            if extra(): print("skipping star")
            # skip one, try again
            actual.popleft()
            continue

        return True
    if extra(): print("ended loop with", wanted, actual)

    if return_exact:
        if extra(): print("exact match:", len(actual) == len(wanted) == 0, path, query_path)
        return not (len(actual) == len(wanted) == 0)

    if len(actual) > 0:
        # we have gone too far inside
        return True
    return False


def find_from_wml(node, path, query):
    printable_path = [n.get_name() for n in path]
    if extra(): print("searching", printable_path, query)
    if path_invalidates_match(path, query[0]):
        if extra(): print("path invalidates match")
        return
    else:
        if extra(): print("match still possible")
    if len(path) > len(query[0]) and "*" not in query[0]:
        # only looked trees of limited depth
        return
    if isinstance(node, wmlparser3.TagNode):
        for child in node.get_all():
            if isinstance(child, wmlparser3.TagNode):
                find_from_wml(child, path + [child], query)
            else:
                find_from_wml(child, path, query)
    elif isinstance(node, wmlparser3.AttributeNode):
        if query_matches(node, path, query):
            printable_ids = [n.get_text_val("id") for n in path]
            if prod(): print("found match at", printable_path, printable_ids)


def parse_wml_query(query):
    path_wanted = []
    attr_wanted = None
    if query.startswith(">>"):
        path_wanted.append("*")
        query = query[2:]
    elif query.startswith(">"):
        path_wanted.append("?")
        query = query[1:]

    query = query.split(">")
    for item in query:
        if item == "":
            path_wanted.append("*")
        elif len(item) > 2 and item[0] == "[" and item[-1] == "]":
            path_wanted.append(item[1:-1])
        else:
            # TODO parse attr filter
            if "==" in item:
                item = item.split("==", 1)
                attr_wanted = (item[0], item[1])
            else:
                attr_wanted = (item, "*")
    return path_wanted, attr_wanted


# query made of tag path, ending with single attribute request
# make query list of queries, used as and conditions
# query = parse_wml_query(">[damage]>add==1")
parsed_query = parse_wml_query(">>[unit_type]>>[damage]>add==2")
print(parsed_query)
# print(query_matches(None, ["unit_type", "attack", "specials"], query))

if perf():
    import timeit

    start_time = timeit.default_timer()
    find_from_wml(root_node, [], parsed_query)
    elapsed = timeit.default_timer() - start_time
    print(elapsed)  # obsolete
else:
    find_from_wml(root_node, [], parsed_query)
