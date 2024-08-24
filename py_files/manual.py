#!/usr/bin/python3
from collections import defaultdict
from os.path import join

import rav_parser

type_stats = defaultdict(int)


def result_function(description, path, attributes):
    if "type" in attributes[2] and "damage" in attributes[2] and "number" in attributes[2]:
        attack_type = attributes[2]["type"]
        weight = int(attributes[2]["damage"])*int(attributes[2]["number"])
        type_stats[attack_type] = type_stats[attack_type] + weight
    else:
        print(attributes)


addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)


parsed_query = [
    rav_parser.parse_wml_query("[units]/[unit_type]/[attack]")
]
output_keys = ["type", "level", "id", "number", "damage"]

rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, result_function)

print(type_stats)
