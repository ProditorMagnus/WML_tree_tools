import rav_parser
from typing import List, Dict

Attributes = Dict[str, str]

addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)


def check_damage_types():
    """Finds nonstandard resists and damage types"""

    def damage_type_function(description, path, attributes):
        """Shows nonstandard damage types"""
        damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce", "secret", "insects"]
        damage_type = attributes[2]["type"]
        if damage_type not in damage_types:
            print("damage_type_function", damage_type, description, path, attributes)

    def resist_type_function(description, path, attributes):
        """Shows nonstandard resists"""
        damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce"]
        resists = attributes[2]
        for res in resists:
            if res not in damage_types:
                print("resist_type_function", res, description, path, attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/type")]
    output_keys = ["id", "type"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, damage_type_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[resistance]/")]
    output_keys = ["id", "type", "*"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, resist_type_function)


def check_movetype_names():
    """Finds missing or unknown movetypes"""
    # Core movetypes
    known_movetypes = ['smallfoot', 'orcishfoot', 'largefoot', 'armoredfoot', 'elusivefoot', 'mounted', 'woodland',
                       'woodlandfloat', 'treefolk', 'fly', 'smallfly', 'lightfly', 'deepsea', 'swimmer', 'naga',
                       'float', 'mountainfoot', 'dwarvishfoot', 'gruefoot', 'undeadfoot', 'undeadfly', 'undeadspirit',
                       'spirit', 'lizard', 'none', 'scuttlefoot', 'rodentfoot', 'drakefly', 'drakeglide', 'drakeglide2',
                       'drakefoot', 'dunefoot', 'dunearmoredfoot', 'dunehorse', 'dunearmoredhorse']

    def movetype_name_list_function(description, path, attributes):
        """Shows missing movetypes resists"""
        known_movetypes.append(attributes[1]["name"])

    def movetype_name_check_function(description, path, attributes):
        movetype = attributes[1]["movement_type"]
        if movetype not in known_movetypes:
            print("unknown movetype", movetype, description, path, attributes)

    def movetype_missing_function(description, path, attributes):
        print("unit without movetype", description, path, attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[movetype]/name")]
    output_keys = ["id", "name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, movetype_name_list_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/movement_type")]
    output_keys = ["id", "movement_type"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, movetype_name_check_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/movement_type!")]
    output_keys = ["id", "movement_type"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, movetype_missing_function)


def find_id_without_prefix():
    unprefixed_ids = set()
    common_ids = ["leadership", "submerge", "nightstalk", "regenerates", "skirmisher", "feeding", "illumination",
                  "steadfast", "teleport", "ambush", "healing", "concealment", "curing"]

    def on_id(description, path, attributes: List[Attributes]):
        for path_attributes in attributes:
            if "id" in path_attributes:
                value = path_attributes["id"]
                if not value.startswith("AE_"):
                    if value not in common_ids:
                        unprefixed_ids.add(value)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[abilities]/[?]")]
    output_keys = ["id"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/[specials]/[?]")]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    print("unprefixed ids", unprefixed_ids)


def check_duplicate_abilities():
    units_with_ability = set()
    units_with_multiple_abilities = set()

    def on_id(description, path, attributes: List[Attributes]):
        unit = attributes[1]["id"]
        if unit in units_with_ability:
            units_with_multiple_abilities.add(unit)
        units_with_ability.add(unit)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[abilities]")]
    output_keys = ["id"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    print("Duplicate abilities", units_with_multiple_abilities)


def check_duplicate_resists():
    units_with_resist = set()
    units_with_multiple_resists = set()

    def on_id(description, path, attributes: List[Attributes]):
        unit = attributes[1]["id"]
        if unit in units_with_resist:
            units_with_multiple_resists.add(unit)
        units_with_resist.add(unit)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[resistance]")]
    output_keys = ["id"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    print("Duplicate resistance", units_with_multiple_resists)


def check_duplicate_defense():
    units_with_tag = set()
    units_with_multiple_tags = set()

    def on_id(description, path, attributes: List[Attributes]):
        unit = attributes[1]["id"]
        if unit in units_with_tag:
            units_with_multiple_tags.add(unit)
        units_with_tag.add(unit)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[defense]")]
    output_keys = ["id"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    print("Duplicate defense", units_with_multiple_tags)


def check_filter_attack():
    names = set()

    def on_id(description, path, attributes: List[Attributes]):
        # print(description, path, attributes)
        for key, value in attributes[2]:
            if key == "name":
                names.add(value)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[event]/[filter_attack]")]
    output_keys = ["id", "name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    print("names with filter_attack", names)


def check_all():
    check_damage_types()
    check_movetype_names()
    find_id_without_prefix()
    check_duplicate_abilities()
    check_duplicate_resists()
    check_duplicate_defense()
    # TODO check weapon specials


# check_filter_attack()
check_all()
