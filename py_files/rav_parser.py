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
            pickle.dump(root_node)


def find_inner_from_path(path, tag):
    for i in range(len(path) - 1, -1, -1):
        node = path[i]
        if node.get_name() == tag:
            return node


def explore_wml(node, path):
    printable_path = [n.get_name() for n in path]
    if isinstance(node, wmlparser3.TagNode):
        try:
            name = node.get_name()
        except:
            if extra(): print("getting name failed for", printable_path)
            node.name = "no_name_defined"
            name = "no_name_defined"

        if name == "event":
            if node.get_text_val("id") is None:
                if "unit_type" in printable_path:
                    if debug(): print(find_inner_from_path(path, "unit_type").get_text_val("id"),
                                      "has event without id", node.get_text_val("name"), printable_path)
                    if prod(): print("MISSING_ID:", find_inner_from_path(path, "unit_type").get_text_val("id"), ":",
                                     node.get_text_val("name"))
                else:
                    if extra(): print("found event without id at", printable_path, node.get_text_val("name"),
                                      node.debug()[:100])

                    # input()
        for child in node.get_all():
            explore_wml(child, path + [child])


def query_matches(node, path, query):
    if path_invalidates_match(path, query[0], True):
        return False
    # tag_path = path # for dry testing
    # tag_path = [n.get_name() for n in path]  # not for dry testing
    # # TODO add support for *
    # query_path = query[0]
    # if debug() and "unit_type" not in tag_path:
    #     # only for debug
    #     return False
    # if debug() and len(tag_path) != len(query_path):
    #     return False
    # query_pos = 0
    # tag_pos = 0
    # found_pos = 0
    # i = 0
    # while found_pos < len(query_path) and i < 20 and tag_pos < len(tag_path) and query_pos < len(query_path):
    #     i += 1
    #     if tag_path[tag_pos] == query_path[query_pos]:
    #         if extra(): print("found", tag_pos, query_pos, tag_path, query_path)
    #         query_pos += 1
    #         tag_pos += 1
    #         found_pos += 1
    #     else:
    #         if extra():
    #             print("* not supported", tag_path, query_path)
    #             input()
    #         return False
    #         # TODO handle *
    # if found_pos < len(query_path):
    #     # so loop ended too quickly
    #     if debug(): print("loop ended at", found_pos, "expected", len(query_path))
    #     return False
    # so it found suitable tag place
    # check attribute then
    attr_query = query[1]
    if attr_query is not None:
        if node.get_name() != attr_query[0]:
            return False
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
    # if there is no way that this path can match query

    if extra(): print("inside path_invalidates_match", path, query_path)

    # this is not enough to say for the future
    # if len(path) < len([tag for tag in query_path if tag != "*"]):
    #     if extra(): print("path is too long to be possible match", path, query_path)
    #     return True

    wanted = deque(query_path)
    actual = deque(path)

    star_open = False
    while len(wanted) > 0 and len(actual) > 0:
        # if
        w = wanted[0]
        a = actual[0]
        if w == "*":
            if debug(): print("star opened")
            star_open = True
            wanted.popleft()
            continue
        if a == w or w == "?":
            if debug(): print("a is w", a, w)
            wanted.popleft()
            actual.popleft()
            star_open = False
            continue
        if star_open:
            if debug(): print("skipping star")
            # skip one, try again
            actual.popleft()
            continue

        return True
    if debug(): print("ended loop with", wanted, actual)

    if return_exact:
        if debug(): print("exact match:", len(actual) == len(wanted) == 0, path, query_path)
        return not (len(actual) == len(wanted) == 0)

    if len(actual) > 0:
        # we have gone too far inside
        return True
    return False
    # star_open = False
    # p = 0
    # q = 0
    # while q < len(query_path):
    #     # remember that any amount is allowed, and skip if there are multiple
    #     if query_path[q] == "*":
    #         print("start_found")
    #         star_open = True
    #         q += 1
    #     elif path[p] == query_path[q]:
    #         # matches, so advance past this, close star if it was open
    #         # therefore, nongreedy match only supported
    #         star_open = False
    #         q += 1
    #         p += 1
    #     elif star_open:
    #         # advance haystick position
    #         print("star_open")
    #         p += 1
    #     else:
    #         # different tag than was was expected
    #         if extra(): print("different tag than expected", path[p])
    #         return True
    # return False


def find_from_wml(node, path, query):
    printable_path = [n.get_name() for n in path]
    if debug(): print("searching", [n.get_name() for n in path], query)
    if path_invalidates_match(path, query[0]):
        # TODO this must find when there is first difference, like era vs units
        if extra(): print("path invalidates match")
        if debug(): print("path invalidates match")
        return
    else:
        if debug(): print("match still possible")
    if len(path) > len(query[0]) and not "*" in query[0]:
        # only looked trees of limited depth
        return
    if isinstance(node, wmlparser3.TagNode):
        for child in node.get_all():
            if isinstance(child, wmlparser3.TagNode):
                find_from_wml(child, path + [child], query)
            else:
                find_from_wml(child, path, query)
    elif isinstance(node, wmlparser3.AttributeNode):
        # check if something is being searched from this path
        # debug
        if printable_path[0] != "units" or printable_path[1] != "unit_type":
            return
        if query_matches(node, path, query):
            printable_ids = [n.get_text_val("id") for n in path]
            if prod(): print("found match at", printable_path, printable_ids)
            # else:
            # if extra(): print("no match at",printable_path)


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
            # this should be attribute query then
            # TODO parse attr filter
            if "==" in item:
                item = item.split("==", 1)
                attr_wanted = (item[0], item[1])
            else:
                attr_wanted = (item, "*")
    return path_wanted, attr_wanted


# explore_wml(root_node, [])
# query made of tag path, ending with single attribute request
# make query list of queries
# query = parse_wml_query(">[damage]>add==1")
query = parse_wml_query(">>[unit_type]>>[damage]>add==2")
print(query)
# print(query_matches(None, ["unit_type", "attack", "specials"], query))

if perf():
    import timeit

    start_time = timeit.default_timer()
    find_from_wml(root_node, [], query)
    elapsed = timeit.default_timer() - start_time
    print(elapsed)  # 1.1117582430399235, 0.9999734076674559, 1.1983144193424229, 1.0922506677241397
# and when removed that check 0.9830210289366565, 0.9595633259076966,
# most likely something was double-check and something that should be checked was not
else:
    find_from_wml(root_node, [], query)
