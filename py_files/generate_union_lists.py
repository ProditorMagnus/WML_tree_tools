#!/usr/bin/python3
from os.path import join
from typing import List, Tuple

import rav_parser

recruits = set()
leaders = set()


def result_function(description, path, attributes: List[List[Tuple[str, str]]]):
    if attributes[0][0][1] != "Ageless Era":
        return
    value: str
    key: str
    for (key, value) in attributes[1]:
        if key == "leader":
            add_all(value, leaders)
        if key == "random_leader":
            add_all(value, leaders)
        if key == "recruit":
            add_all(value, recruits)
    print(attributes)


def add_all(value, var):
    split = value.split(",")
    for unit in split:
        if unit.startswith("AE_"):
            var.add(unit)


addonId = "Ageless_Era"
root_node = rav_parser.parse_root_node(join("..", "preprocessed_addon", addonId, "_main.cfg"))

parsed_query = [rav_parser.parse_wml_query("[era]/[multiplayer_side]")]
output_keys = ["id", "leader", "random_leader", "recruit"]

rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, result_function)

with open("union_recruits.txt", "w", encoding="utf8") as f:
    f.write(",".join(recruits))
with open("union_leaders.txt", "w", encoding="utf8") as f:
    f.write(",".join(leaders))
