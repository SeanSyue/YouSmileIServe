import json
from itertools import permutations


def get_query(menu):
    """ Generate all combinations of text query of meal options """
    comb = list()
    for i in range(2, len(menu) + 1):
        comb.extend(list(permutations(menu, i)))
    query_multi = [' and '.join(map(str, x)) + ' are' for x in comb]
    query_single = ['only ' + x + ' is' for x in menu]
    return query_single + query_multi


with open('../menu/rice_menu.txt') as r_menu:
    RICE_MENU = [x.strip() for x in r_menu.readlines()]
with open('../menu/noodle_menu.txt') as n_menu:
    NOODLE_MENU = [x.strip() for x in n_menu.readlines()]

if __name__ == '__main__':
    with open('./actions_8_cancel_conversation.json') as f:
        data = json.loads(f.read())

    type_rice_opt = list(filter(lambda x: x['name'] == '$Rice_options', data['types']))[0]
    type_noodle_opt = list(filter(lambda x: x['name'] == '$Noodle_options', data['types']))[0]
    type_meal_specific = list(filter(lambda x: x['name'] == '$Meal_specific', data['types']))[0]
    type_meal_rice = list(filter(lambda x: x['name'] == '$Meal_rice', data['types']))[0]
    type_meal_noodle = list(filter(lambda x: x['name'] == '$Meal_noodle', data['types']))[0]

    rice_query = get_query(RICE_MENU)
    noodle_query = get_query(NOODLE_MENU)

    type_rice_opt['entities'] = [{"key": x, "synonyms": [x]} for x in rice_query]
    type_noodle_opt['entities'] = [{"key": x, "synonyms": [x]} for x in noodle_query]
    type_meal_specific['entities'] = [{"key": x, "synonyms": [x]} for x in RICE_MENU+NOODLE_MENU]
    type_meal_rice['entities'] = [{"key": x, "synonyms": [x]} for x in RICE_MENU]
    type_meal_noodle['entities'] = [{"key": x, "synonyms": [x]} for x in NOODLE_MENU]

    with open('./actions_9_more_menu.json', 'w+') as out:
        print(json.dumps(data, indent=4), file=out)
