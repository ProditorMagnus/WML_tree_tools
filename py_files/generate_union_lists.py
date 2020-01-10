#!/usr/bin/python3
from typing import List, Tuple, Dict

import rav_parser

recruits = set()
leaders = set()


def get_result_function(eraId):
    def result_function(description, path, attributes: List[Dict[str, str]]):
        if attributes[0]["id"] != eraId:
            return
        keys = attributes[1].keys()
        if "leader" in keys:
            add_all(attributes[1]["leader"], leaders, eraId)
        if "random_leader" in keys:
            add_all(attributes[1]["random_leader"], leaders, eraId)
        if "recruit" in keys:
            add_all(attributes[1]["recruit"], recruits, eraId)

    return result_function


def add_all(value, var, eraId):
    split = value.split(",")
    for unit in split:
        if unit.startswith("AE_") or "Ageless" not in eraId:
            var.add(unit)


# ageless
addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)

parsed_query = [rav_parser.parse_wml_query("[era]/[multiplayer_side]")]
output_keys = ["id", "leader", "random_leader", "recruit"]

rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, get_result_function("Ageless Era"))

with open("union_recruits.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(recruits)))
with open("union_leaders.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(leaders)))

# default
recruits = set()
leaders = set()
root_node = rav_parser.load_core_node()

rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, get_result_function("era_dunefolk"))

with open("default_recruits.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(recruits)))
with open("default_leaders.txt", "w", encoding="utf8") as f:
    f.write(",".join(sorted(leaders)))
