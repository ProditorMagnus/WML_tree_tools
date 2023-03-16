from collections import defaultdict

import rav_parser
from typing import List, Dict

Attributes = Dict[str, str]

addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId, False)


def check_units():
    unit_levels = {}
    unit_parents = defaultdict(set)

    def unit_check_function(description, path, attributes):
        unit_id = attributes[1]["id"]
        if "description" in attributes[1]:
            desc = attributes[1]["description"]
            if "<" in desc:
                print(unit_id, "has <", desc)
        if "level" not in attributes[1]:
            print(unit_id, "has no level")
            return
        unit_level = attributes[1]["level"]
        unit_levels[unit_id] = int(unit_level)
        if "advances_to" not in attributes[1]:
            print(unit_id, "has no advances_to")
            return
        advances_to = attributes[1]["advances_to"]
        if advances_to is not None:
            advances_to = advances_to.split(",")
            for advancement in advances_to:
                unit_parents[advancement].add(unit_id)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]")]
    output_keys = ["id", "type", "level", "advances_to", "description"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, unit_check_function)

    supported_units = set()
    unknown_units = set()
    last_size = 0
    for unit in unit_levels:
        if unit_levels[unit] >= 2:
            supported_units.add(unit)
        else:
            unknown_units.add(unit)

    # parents of all supported units are supported
    while len(unknown_units) != last_size:
        last_size = len(unknown_units)
        print("iteration on unknown units")
        additions = set()
        for supported_unit in supported_units:
            for unit in unit_parents[supported_unit]:
                additions.add(unit)
                if unit in unknown_units:
                    unknown_units.remove(unit)
        supported_units = supported_units.union(additions)
    print(len(unit_levels), len(supported_units), len(unknown_units))
    print(unknown_units)


check_units()
