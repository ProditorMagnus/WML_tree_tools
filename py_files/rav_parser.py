#!/usr/bin/env python3
# encoding: utf-8

import pickle
from os.path import join, isfile
from collections import deque
import wmlparser3

#		 01234567
mode = 0b11001000  # program settings


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


def load_root_node():
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
    return root_node


def query_matches(node, path, query, exact=True):
    if path_invalidates_match(path, query[0], exact):
        return False
    attr_query = query[1]
    if attr_query is not None:
        attr_node = node.get_all(att=attr_query[0])
        if not len(attr_node):
            # if no such attribute, check if this was wanted
            # TODO when node is tagnode not attr anymore, might need to use +[node] for all places where is path_invalidates_match
            # TODO  + [node] breaks checking if event id does not exist, but removing it breaks if attribute does not exist check on lower level
            try:
                if attr_query[1](None) and not path_invalidates_match(path, query[0], True):
                    if extra(): print("path invalidate match when no attr",
                                      path_invalidates_match(path + [node], query[0], True))
                    if extra(): print("query matches for attr not existing", [n.get_name() for n in path], attr_node)
                    return True
                return False
            except:
                return False
        attr_node = attr_node[0]
        attr_value = attr_node.get_text()
        try:
            attr_value = int(attr_value)
        except:
            pass
        return attr_query[1](attr_value)
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
        wanted = [i for i in wanted if i != "*"]
        if extra(): print("exact match:", len(actual) == len(wanted) == 0, path, query_path)
        if star_open:
            return len(wanted) != 0
        return not (len(actual) == len(wanted) == 0)

    if len(actual) > 0 and not star_open:
        # we have gone too far inside
        return True
    return False


def find_from_wml(node, path, query_list, output_keys, callable_function):
    printable_path = [n.get_name() for n in path]
    if extra(): print("searching", printable_path, query_list)
    # for each query, check that current path can be what is needed
    for query in query_list:
        query_path = query[0]
        if path_invalidates_match(path, query_path):
            if extra(): print("path invalidates match")
            return
        else:
            if extra(): print("match still possible")
        if len(path) > len(query_path) and "*" not in query_path:
            # only looked trees of limited depth
            return
        break  ### TODO think if should be checked for others
    if isinstance(node, wmlparser3.TagNode):
        # here try to match instead
        # check if something is allowed to come after node with attribute
        matches = False
        for query in query_list:
            if query_matches(node, path, query):
                matches = True
            else:
                lesser_matches = False
                if matches:
                    # try if it matches with less path
                    for i in range(len(path)):
                        if query_matches(path[i], path[:i], query, False):
                            lesser_matches = True
                            break
                if not lesser_matches:
                    matches = False
                    break

        if matches:
            printable_ids = []
            for n in path:
                printable_values = []
                for output_key in output_keys:
                    val = n.get_text_val(output_key)
                    if val is not None:
                        printable_values.append((output_key, val))
                printable_ids.append(printable_values)

            if prod(): callable_function("found match at", printable_path, printable_ids)

        for child in node.get_all():
            if isinstance(child, wmlparser3.TagNode):
                find_from_wml(child, path + [child], query_list, output_keys, callable_function)
            else:
                find_from_wml(child, path, query_list, output_keys, callable_function)
    elif isinstance(node, wmlparser3.AttributeNode):
        # TOO late to try to match here
        return


def parse_wml_query(query):
    # TODO return list of queries, and then output_keys
    output_keys = ["id"]
    if "~" in query:
        query, output_keys = query.split("~", 1)
        output_keys = output_keys.split(",")

    operators = {
        "==": lambda x, y: y == x,
        "!=": lambda x, y: y != x,
        ">=": lambda x, y: y >= x,
        ">": lambda x, y: y > x,
        "<=": lambda x, y: y <= x,
        "<": lambda x, y: y < x,
        "!": lambda x, y: y is None
    }

    path_wanted = []
    attr_wanted = None
    if query.startswith("//"):
        path_wanted.append("*")
        query = query[2:]
    elif query.startswith("/"):
        path_wanted.append("?")
        query = query[1:]

    query = query.split("/")
    for item in query:
        if item == "":
            path_wanted.append("*")
        elif len(item) > 2 and item[0] == "[" and item[-1] == "]":
            path_wanted.append(item[1:-1])
        else:
            found_operator = False
            for operator in sorted(operators, key=lambda x: len(x[0])):
                if operator in item:
                    item = item.split(operator, 1)
                    try:
                        item[1] = int(item[1])
                    except:
                        pass
                    attr_wanted = [item[0], lambda x: operators[operator](item[1], x)]
                    found_operator = True
                    break
            if not found_operator:
                if debug(): print("attr check set to not None")
                attr_wanted = (item, lambda x: x is not None)
        if attr_wanted is None:
            attr_wanted = (item, lambda x: True)
    return [path_wanted, attr_wanted, output_keys]


# query made of tag path, ending with single attribute request
# make query list of queries, used as and conditions
# query = parse_wml_query(">[damage]>add==1")
# parsed_query = parse_wml_query("[units]/[unit_type]//[damage]/add<0")
# parsed_query = parse_wml_query("[units]/[unit_type]/[attack]/damage>=33~id,number,damage")
# parsed_query = parse_wml_query("[units]/[unit_type]/id~id,movement_type")
# parsed_query = parse_wml_query("//[movetype]/name~name")
# parsed_query = parse_wml_query("[units]/[unit_type]/experience==100~id,experience,level")
# parsed_query = parse_wml_query(">>[unit_type]>>add==2")
# parsed_query = parse_wml_query("//id")
# parsed_query = [parse_wml_query("[units]/[unit_type]/level==1"),
#                 parse_wml_query("[units]/[unit_type]/hitpoints>=45")]
# output_keys = ["id", "cost", "hitpoints"]
# parsed_query = [parse_wml_query("[units]/[unit_type]/[event]/id!")]
# output_keys = ["id", "name", "first_time_only"]
# parsed_query = [parse_wml_query("[units]/[unit_type]/level==1")]
# output_keys = ["id"]
# When generating lists, replace
# .*?'(AE_[A-Za-z_0-9]+)'
# "\1",

# print(query_matches(None, ["unit_type", "attack", "specials"], query))
# parsed_query[1][1] = lambda x: x % 3 == 1

if __name__ == '__main__':
    parsed_query = [parse_wml_query("[units]/[unit_type]/level==0")]
    output_keys = ["id"]
    print(parsed_query)

    root_node = load_root_node()
    if perf():
        import timeit

        start_time = timeit.default_timer()
        find_from_wml(root_node, [], parsed_query, output_keys, print)
        elapsed = timeit.default_timer() - start_time
        print(elapsed)  # obsolete
    else:
        find_from_wml(root_node, [], parsed_query, output_keys, print)
