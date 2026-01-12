#!/usr/bin/python3
from collections import defaultdict
from os.path import join

import rav_parser

movetypes = {}
unit_resistance = {}
unit_final_resistance = {}

def movetype_function(description, path, attributes):
    movetypes[attributes[1]["name"]] = {}
    for res in attributes[2]:
        movetypes[attributes[1]["name"]][res] = attributes[2][res]

def resistance_function(description, path, attributes):
    unit_resistance[attributes[1]["id"]] = {}
    for res in attributes[2]:
        unit_resistance[attributes[1]["id"]][res] = attributes[2][res]

def summary_function(description, path, attributes):
    unit_type = attributes[1]["id"]
    effective_res = {}
    if "movement_type" in attributes[1] and attributes[1]["movement_type"] in movetypes:
        for res in movetypes[attributes[1]["movement_type"]]:
            effective_res[res] = movetypes[attributes[1]["movement_type"]][res]
    if unit_type in unit_resistance:
        for res in unit_resistance[unit_type]:
            effective_res[res] = unit_resistance[unit_type][res]
    unit_final_resistance[unit_type] = effective_res



addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)

output_keys = ["*"]

movetype_query = [rav_parser.parse_wml_query("[units]/[movetype]/[resistance]")]
rav_parser.find_from_wml(root_node, [], movetype_query, output_keys, movetype_function)

resistance_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[resistance]")]
rav_parser.find_from_wml(root_node, [], resistance_query, output_keys, resistance_function)

type_query = [rav_parser.parse_wml_query("[units]/[unit_type]/level==1")]
rav_parser.find_from_wml(root_node, [], type_query, output_keys, summary_function)

res_distribution = {}
res_values = {}
for unit in unit_final_resistance:
    for res in unit_final_resistance[unit]:
        value = int(unit_final_resistance[unit][res])
        if res not in res_values:
            res_values[res] = []
        res_values[res].append(value)
        # group by weak/strong/neutral
        if value <= 109 and value >= 91:
            value = 100
        if value > 100:
            value = 101
        if value < 100:
            value = 99
        if value not in res_distribution:
            res_distribution[value] = defaultdict(int)
        res_distribution[value][res] = res_distribution[value][res]+1

print(res_distribution)
for res in res_values:
    print(res, sum(res_values[res])/len(res_values[res]))
