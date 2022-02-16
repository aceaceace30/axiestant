import math

CLASS_ADVANTAGE_MULTIPLIER = 1.15
CLASS_DISADVANTAGE_MULTIPLIER = 0.85
SAME_CLASS_MULTIPLIER = 1.1
SPECIAL_CLASS_MULTIPLIER = 1.075
ATTACK_UP_MULTIPLIER = 1.2


AXIE_GROUP = {
    1: ['Beast', 'Bug', 'Mech'],
    2: ['Plant', 'Reptile', 'Dusk'],
    3: ['Aquatic', 'Bird', 'Dawn'],
}

AXIE_CLASS_COUNTER_MAPPING = {
    1: {
        '+': 2, # Plant/Reptile/Dusk
        '-': 3, # Aquatic/Bird/Dawn
    },
    2: {
        '+': 3,
        '-': 1,
    },
    3: {
        '+': 1,
        '-': 2,
    },
}

AXIE_CLASSES = list()
for group in AXIE_GROUP.values():
    AXIE_CLASSES += [axie_class for axie_class in group]


def get_attack_up_bonus_multiplier(card_name, target_class, attack_up_multiplier):
    if (card_name == 'Fish Hook' and target_class == 2):
        attack_up_multiplier = ATTACK_UP_MULTIPLIER
    elif (card_name == 'Clam Slash' and target_class == 1):
        attack_up_multiplier = ATTACK_UP_MULTIPLIER
    elif (card_name == 'Cuckoo'):
        attack_up_multiplier += .2
    else:
        attack_up_multiplier = 1
    return attack_up_multiplier

def get_class_bonus(attacker_class, card_class):
    multiplier = 1
    if (attacker_class == 'Dusk' and card_class in ['Plant', 'Reptile']) or \
            (attacker_class == 'Mech' and card_class in ['Beast', 'Bug']) or \
            (attacker_class == 'Dawn' and card_class in ['Bird', 'Aquatic']):
        multiplier = SPECIAL_CLASS_MULTIPLIER

    elif attacker_class == card_class:
        multiplier = SAME_CLASS_MULTIPLIER

    return multiplier

def get_class_advantage_disadvantage_bonus(card_class, target_class):
    group_number = 0
    for group_num, axie_list in AXIE_GROUP.items():
        if card_class in axie_list:
            group_number = group_num
            break

    plus_minus_counter = AXIE_CLASS_COUNTER_MAPPING[group_number]
    operator = None  # None means card damage will be the same
    for opr, axie_group_num in plus_minus_counter.items():
        if target_class == axie_group_num:
            operator = opr

    if operator == '+':
        multiplier = CLASS_ADVANTAGE_MULTIPLIER
    elif operator == '-':
        multiplier = CLASS_DISADVANTAGE_MULTIPLIER
    else:
        multiplier = 1
    return multiplier

def get_card_combo_bonus(card_count, attacker_skill, card_attack):
    combo_card_bonus = 0
    if card_count > 1:
        combo_card_bonus = card_attack * (attacker_skill * 0.55 - 12.25) / 100 * 0.985

    return combo_card_bonus


def get_crit_multiplier(card_name, card_count):
    multiplier = 1
    if card_name == 'Single Combat' and card_count > 2:
        multiplier = 2
    return multiplier


def calculate_damage(axie, target_class, part_name, card_count, attack_up_current_multiplier):

    attacker_class = axie.class_
    attacker_skill = axie.stats['skill']

    ability_details = axie.get_ability_details(part_name)
    card_name = ability_details['name']
    card_class = ability_details['class']
    card_attack = ability_details['attack']

    same_class_multiplier = get_class_bonus(attacker_class, card_class)
    class_adv_dis_multiplier = get_class_advantage_disadvantage_bonus(card_class, target_class)
    card_attack_applied_multiplier = card_attack * same_class_multiplier * class_adv_dis_multiplier
    combo_bonus = get_card_combo_bonus(card_count, attacker_skill, card_attack_applied_multiplier)

    attack_up_multiplier = get_attack_up_bonus_multiplier(card_name, target_class, attack_up_current_multiplier)

    crit_multiplier = 1 # get_crit_multiplier(card_name, card_count)

    total = math.floor((card_attack_applied_multiplier * crit_multiplier + combo_bonus) * attack_up_current_multiplier)

    print('---------')
    print('card_name', card_name)
    print('card_attack', card_attack)
    print('combo_bonus', combo_bonus)
    print('attack_up_multiplier', attack_up_multiplier)
    print('attack_up_current_multiplier', attack_up_current_multiplier)
    print('crit_multiplier', crit_multiplier)
    print('total', total)

    return total, attack_up_multiplier
