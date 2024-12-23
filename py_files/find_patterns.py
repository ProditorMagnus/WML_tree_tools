import rav_parser
from typing import List, Dict

Attributes = Dict[str, str]

addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId, False)

# unit -> base unit
unit_to_base_unit = {}
units = {}


def populate_base_unit_data():
    def base_unit_function(description, path, attributes):
        """Collects base units"""
        unit_to_base_unit[attributes[1]["id"]] = attributes[2]["id"]

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[base_unit]")]
    output_keys = ["id"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, base_unit_function)


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
        damage_types = ["arcane", "blade", "cold", "fire", "impact", "pierce", "secret"]
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


def check_range():
    """Finds nonstandard attack ranges"""

    def range_check_function(description, path, attributes):
        known_ranges = ["melee", "ranged", "artillery", "sapper", "kamikaze", "study"]
        attack_range = attributes[2]["range"]
        if attack_range not in known_ranges:
            print("range_check_function", attack_range, description, path, attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/range")]
    output_keys = ["id", "range"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, range_check_function)


def check_movetype_names():
    """Finds missing or unknown movetypes"""
    # Core movetypes
    known_movetypes = ['smallfoot', 'orcishfoot', 'largefoot', 'armoredfoot', 'elusivefoot', 'mounted', 'woodland',
                       'woodlandfloat', 'treefolk', 'fly', 'smallfly', 'lightfly', 'deepsea', 'swimmer', 'naga',
                       'float', 'mountainfoot', 'dwarvishfoot', 'gruefoot', 'undeadfoot', 'undeadfly', 'undeadspirit',
                       'spirit', 'lizard', 'none', 'scuttlefoot', 'rodentfoot', 'drakefly', 'drakeglide', 'drakeglide2',
                       'drakefoot', 'dunefoot', 'dunearmoredfoot', 'dunehorse', 'dunearmoredhorse']
    known_movetypes = []  # when loading _main.cfg, these are not needed

    def movetype_name_list_function(description, path, attributes):
        movetypeName = attributes[1]["name"]
        if movetypeName in known_movetypes:
            print("duplicate movetype", movetypeName, description, path, attributes)
        known_movetypes.append(movetypeName)

    def movetype_name_check_function(description, path, attributes):
        movetype = attributes[1]["movement_type"]
        if movetype not in known_movetypes:
            print("unknown movetype", movetype, description, path, attributes)

    def movetype_missing_function(description, path, attributes):
        if attributes[1]["id"] not in unit_to_base_unit:
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
    whitelist_ids = [
        # mainline ids
        "leadership", "submerge", "nightstalk", "regenerates", "skirmisher", "feeding", "illumination",
        "steadfast", "teleport", "ambush", "healing", "concealment", "curing", "berserk", "plague", "firststrike",
        "slow", "marksman", 'stun', 'absorb', 'deflect', 'magical', 'poison', 'backstab', 'diversion', 'swarm',
        'drains', 'charge', 'burrow',
        # non-event based non-filtered ids are not important
        'rage5', 'rage4', "rage3", "rage2", "leader_moral", "counter",
        "undeadheal8", "undeadheal5", "undeadheal4",
        "aoadiscipline", "protection", "darkillumination", "eeawdiscipline", "drumbeat", "inspire1", 'inspire2',
        'mountainambush',
        'low_upkeep', 'small cold protection', 'auraofweakness', 'caveambush', 'dauntless', 'self_repair',
        'regenerates4', 'terror', 'unlucky', 'snow_cover', 'repair', 'snow_hide', 'aoaRepair',
        'plague_lesser_assimilation', 'delumination', 'swampambush', 'selfheal', 'swamp_lurk', 'distract',
        'flddefender', 'auraoflife', 'reinkarnacja', 'sealpack', 'flawetxt', 'parry', 'defend-only', 'flawe',
        'waterambush', 'steelskin', 'berserker', 'mech_healing', 'rally',
        # false positives
        "plague(AE_efm_pygmies_Toad)", "plague(Fire Ant Egg)", "plague(AE_ext_monsters_Baby_Mudcrawler)",
        "plague(Giant Ant Egg)", 'plague(AE_agl_yokai_Swarm_Spawn)', 'plague(AE_mrc_Blight_Parasite)',
        'plague(AE_rhy_ne_Black_Skeleton)', 'plague(AE_mrc_Blight_Infected)', 'plague(AE_mrc_slavers_Slave)',
        'plague(AE_ele_Skeletal_Corpse)', 'plague(AE_efm_pygmies_Lizard)', 'plague(AE_mrc_infernai_Imp)',
        'plague(AE_mrc_hive_Gnat)', 'plague(AE_rhy_de_Spiderling)', 'plague(AE_myh_Bloodborn)'
    ]
    descriptions = set()

    def on_id(description, path, attributes: List[Attributes]):
        for path_attributes in attributes[2:]:
            if "id" in path_attributes:
                value = path_attributes["id"]
                if not value.startswith("AE_"):
                    if value not in whitelist_ids:
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


def check_filter_attack_event_names():
    names = set()
    allowed_names = {"attack", "attacker_hits", "attacker_misses", "defender_hits", "defender_misses", "attack_end",
                     "last_breath", "die"}

    def on_id(description, path, attributes: List[Attributes]):
        # print(description, path, attributes)
        if "name" in attributes[2]:
            names.add(attributes[2]["name"])

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[event]/[filter_attack]")]
    output_keys = ["id", "name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[event]/[filter_second_attack]")]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)
    clean_names = set()
    for name in names:
        if "," in name:
            clean_names.update(map(lambda x: x.replace(" ", "_"), name.split(",")))
        else:
            clean_names.add(name.replace(" ", "_"))
    invalid_names = clean_names.difference(allowed_names)
    if len(invalid_names) > 0:
        print("all event names with filter_attack", names)
        print("invalid event names with filter_attack", invalid_names)


def check_unit_attribute_amount(attr, limit):
    def attribute_value_function(description, path, attributes):
        if attr not in attributes[1]:
            return
        value = int(attributes[1][attr])
        if value > limit:
            print("attribute_value_function", attr, value, description, path, attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]")]
    output_keys = ["id", attr]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, attribute_value_function)


def find_missing_variation_id():
    def on_id(description, path, attributes: List[Attributes]):
        unit = attributes[1]["id"]
        if "variation_id" not in attributes[2]:
            print("Missing variation_id", attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[variation]")]
    output_keys = ["id", "variation_id", "variation_name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)


def find_missing_race_plural_name():
    def on_id(description, path, attributes: List[Attributes]):
        if "plural_name" not in attributes[1]:
            print("Missing plural_name", attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[race]")]
    output_keys = ["id", "name", "male_name", "female_name", "plural_name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)


def check_unit_xp_level():
    attr = "experience"

    def attribute_value_function(description, path, attributes):
        if attr not in attributes[1]:
            return
        value = int(attributes[1][attr])

        # TODO manually check those with custom amla
        if "advances_to" not in attributes[1] or attributes[1]["advances_to"] == "null":
            if value <= 126:
                print("check_unit_xp_level", attr, value, description, path, attributes)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]")]
    output_keys = ["id", attr, "level", "advances_to"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, attribute_value_function)


def find_duplicate_weapon_name():
    knownAttacks = set()
    def on_id(description, path, attributes: List[Attributes]):
        attackId = attributes[1]["id"] + "__" + attributes[2]["name"]
        if attackId in knownAttacks:
            print("find_duplicate_weapon_name", attackId)
        else:
            knownAttacks.add(attackId)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]")]
    output_keys = ["id", "name"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, on_id)


def check_all():
    populate_base_unit_data()
    check_damage_types()
    check_range()
    check_movetype_names()

    find_id_without_prefix()
    find_missing_variation_id()
    find_missing_race_plural_name()

    check_duplicate_abilities()
    check_duplicate_resists()
    check_duplicate_defense()

    check_filter_attack_event_names()

    check_unit_attribute_amount("hitpoints", 142)
    check_unit_attribute_amount("movement", 12)
    check_unit_attribute_amount("experience", 300)
    # TODO check weapon specials


# check_all()

find_duplicate_weapon_name()
