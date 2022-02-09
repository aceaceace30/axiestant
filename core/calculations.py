import math

CLASS_ADVANTAGE_BONUS = 0.15
CLASS_DISADVANTAGE_LESS = 0.15 * -1
SAME_CLASS_BONUS = 0.10
SPECIAL_CLASS_BONUS = 0.075
ATTACK_UP_BONUS = 0.20


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
        attack_up_multiplier += ATTACK_UP_BONUS
    elif (card_name == 'Clam Slash' and target_class == 1):
        attack_up_multiplier += ATTACK_UP_BONUS
    elif (card_name == 'Cuckoo'):
        attack_up_multiplier += ATTACK_UP_BONUS
    return attack_up_multiplier

def get_class_bonus(attacker_class, card_class, card_attack):
    class_bonus = 0
    if (attacker_class == 'Dusk' and card_class in ['Plant', 'Reptile']) or \
            (attacker_class == 'Mech' and card_class in ['Beast', 'Bug']) or \
            (attacker_class == 'Dawn' and card_class in ['Bird', 'Aquatic']):
        class_bonus = SPECIAL_CLASS_BONUS

    elif attacker_class == card_class:
        class_bonus = SAME_CLASS_BONUS

    return card_attack * class_bonus

def get_class_advantage_disadvantage_bonus(card_class, target_class, card_attack, same_class_bonus):
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
        multiplier = CLASS_ADVANTAGE_BONUS
    elif operator == '-':
        multiplier = CLASS_DISADVANTAGE_LESS
    else:
        multiplier = 0
    return (card_attack + same_class_bonus) * multiplier

def get_card_combo_bonus(card_count, attacker_skill, card_attack,
                         same_class_bonus, class_adv_dis_bonus):
    combo_card_bonus = 0
    if card_count > 1:
        combo_card_bonus = (card_attack + same_class_bonus + class_adv_dis_bonus) * (attacker_skill * 0.55 - 12.25) / 100 * 0.985

    return combo_card_bonus

def calculate_damage(axie, target_class, part_name, card_count, attack_up_current_multiplier):

    attacker_class = axie.class_
    attacker_skill = axie.stats['skill']

    ability_details = axie.get_ability_details(part_name)
    card_name = ability_details['name']
    card_class = ability_details['class']
    card_attack = ability_details['attack']

    same_class_bonus = get_class_bonus(attacker_class, card_class, card_attack)
    class_adv_dis_bonus = get_class_advantage_disadvantage_bonus(card_class, target_class,
                                                                 card_attack, same_class_bonus)
    combo_bonus = get_card_combo_bonus(card_count, attacker_skill,
                                       card_attack, same_class_bonus, class_adv_dis_bonus)

    attack_up_multiplier = get_attack_up_bonus_multiplier(card_name, target_class, attack_up_current_multiplier)
    attack_up_bonus = (card_attack + same_class_bonus + class_adv_dis_bonus + combo_bonus) * attack_up_current_multiplier

    total = math.floor(card_attack + same_class_bonus + class_adv_dis_bonus + combo_bonus + attack_up_bonus)

    print('---------')
    print('card_name', card_name)
    print('card_attack', card_attack)
    print('same_class_bonus', same_class_bonus)
    print('class_adv_dis_bonus', class_adv_dis_bonus)
    print('combo_bonus', combo_bonus)
    print('attack_up_current_multiplier', attack_up_current_multiplier)
    print('attack_up_multiplier', attack_up_multiplier)
    print('attack_up_bonus', attack_up_bonus)
    print('total', total)

    if attack_up_bonus > 0:
        attack_up_multiplier = 0

    return total, attack_up_multiplier
