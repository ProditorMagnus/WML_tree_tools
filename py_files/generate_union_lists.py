#!/usr/bin/python3
from typing import List, Tuple, Dict

import rav_parser

recruits = set()
leaders = set()


def result_function(description, path, attributes: List[Dict[str, str]]):
    if attributes[0]["id"] != "Ageless Era":
        return
    keys = attributes[1].keys()
    if "leader" in keys:
        add_all(attributes[1]["leader"], leaders)
    if "random_leader" in keys:
        add_all(attributes[1]["random_leader"], leaders)
    if "recruit" in keys:
        add_all(attributes[1]["recruit"], recruits)


def add_all(value, var):
    split = value.split(",")
    for unit in split:
        if unit.startswith("AE_"):
            var.add(unit)


addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)

parsed_query = [rav_parser.parse_wml_query("[era]/[multiplayer_side]")]
output_keys = ["id", "leader", "random_leader", "recruit"]

rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, result_function)

with open("union_recruits.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(recruits)))
with open("union_leaders.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(leaders)))
