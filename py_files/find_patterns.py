from os.path import join
import rav_parser

addon_version = "preprocessed_addon_ghype"
root_node = rav_parser.parse_root_node(join("..", addon_version, "_main.cfg"))


def damage_type_function(description, path, attributes):
    """Shows nonstandard damage types"""
    damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce"]
    damage_type = attributes[2][0][1]
    assert attributes[2][0][0] == "type"
    if damage_type not in damage_types:
        print("damage_type_function", damage_type, description, path, attributes)


def resist_type_function(description, path, attributes):
    """Shows nonstandard resists"""
    damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce"]
    resists = attributes[2]
    for res, value in resists:
        if res not in damage_types:
            print("resist_type_function", res, description, path, attributes)


def movetype_resist_type_function(description, path, attributes):
    """Shows nonstandard resists"""
    damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce"]
    resists = attributes[2]
    for res, value in resists:
        if res not in damage_types:
            print("resist_type_function", res, description, path, attributes)


def check_damage_types():
    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/type")]
    output_keys = ["id", "type"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, damage_type_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[resistance]/")]
    output_keys = ["id", "type", "*"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, resist_type_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[movetype]/[resistance]/")]
    output_keys = ["id", "type", "*"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, resist_type_function)


check_damage_types()
