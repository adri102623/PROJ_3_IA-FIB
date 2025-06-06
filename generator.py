import argparse
import os
import random

def generate_test():
    def generate_predicate(genpred):
        arguments = genpred['args']
        predicate = '(' + genpred['name']
        for arg in range(arguments):
            predicate += ' ' + random.choice(genpred['types'][arg]['values'])
        return predicate + ')'

    def generate_day_before(days):
        day_before = ''
        for i in range(len(days) - 1):
            day_before += 4 * ' ' + '(dayBefore ' + days[i] + ' ' + days[i + 1] + ')\n'
        day_before += '\n' + 4 * ' ' + '(mainReady DummyD)'
        day_before += '\n' + 4 * ' ' + '(secondReady DummyD)'
        day_before += '\n' + 4 * ' ' + '(dayMCClassif DummyD DummyC)'
        return day_before + '\n' + 4 * ' ' + '(daySCClassif DummyD DummyC)\n\n'

    def generate_classifications(main_courses, second_courses, categories):
        categories_mc = [5, 3, 6, 4, 6, 0, 1, 6, 2, 2, 2, 0, 4]
        categories_sc = [1, 1, 4, 0, 1, 1, 6, 1, 6, 5, 5, 0]

        categorization = ''
        for index, course in enumerate(main_courses):
            categorization += 4 * ' ' + '(classified ' + course + ' ' + categories[categories_mc[index]] + ')\n'
        for index, course in enumerate(second_courses):
            categorization += 4 * ' ' + '(classified ' + course + ' ' + categories[categories_sc[index]] + ')\n'
        return categorization + '\n'

    def generate_calories(main_courses, second_courses, min_calories, max_calories):
        calories_main = [500, 120, 290, 490, 610, 720, 1000, 240, 600, 760, 480, 320, 410]
        calories_second = [810, 380, 700, 670, 520, 490, 250, 960, 320, 480, 430, 750]

        calories = 4 * ' ' + '(= (minCalories) ' + str(min_calories) + ')\n' + 4 * ' ' + '(= (maxCalories) ' + str(max_calories) + ')\n\n'
        for index, course in enumerate(main_courses):
            calories += 4 * ' ' + '(= (calories ' + course + ') ' + str(calories_main[index]) + ')\n'
        for index, course in enumerate(second_courses):
            calories += 4 * ' ' + '(= (calories ' + course + ') ' + str(calories_second[index]) + ')\n'
        return calories + '\n'

    def generate_prices(main_courses, second_courses):
        prices_main = [8, 7, 5, 12, 10, 15, 5, 10, 16, 9, 11, 6, 13]
        prices_second = [17, 4, 25, 20, 14, 19, 9, 21, 12, 6, 6, 13]

        prices = 4 * ' ' + '(= (totalPrice) 0)\n\n'
        for index, course in enumerate(main_courses):
            prices += 4 * ' ' + '(= (price ' + course + ') ' + str(prices_main[index]) + ')\n'
        for index, course in enumerate(second_courses):
            prices += 4 * ' ' + '(= (price ' + course + ') ' + str(prices_second[index]) + ')\n'
        return prices + '\n'

    data = {
        'objects': [],
        'init': [],
        'goal': []
    }

    # Objects
    day = {
        'values': ['DummyD', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'type': 'day'
    }
    data['objects'].append(day)

    main_course = {
        'values': ['Spaghetti_Bolognese', 'Mediterranean_Salad', 'Vegan_Sandwich', 'Mushroom_risotto',
                   'Guacamole_with_tomatoes', 'Sushi', 'American_burger', 'Broccoli_quiche',
                   'Kirmizi_Mercimek_Corbasi', 'Chinese_Noodles_With_Vegetables', 'Chana_masala',
                   'Chinese_tiger_salad', 'Shumai'],
        'type': 'mainCourse'
    }
    data['objects'].append(main_course)

    second_course = {
        'values': ['Roast_pork_with_prunes', 'Spanish_omelette', 'Paella', 'Tuna_steak', 'Chicken_parmesan',
                   'Lamb_tagine', 'Couscous_meatloaf', 'Coq_au_vin', 'Mapo_tofu', 'Persian_pie', 'Burrito_pie',
                   'Spicy_seafood_stew'],
        'type': 'secondCourse'
    }
    data['objects'].append(second_course)

    dish = {
        'values': main_course['values'] + second_course['values'],
        'type': 'dish'
    }

    category = {
        'values': ['Fish', 'Meat', 'Soup', 'Salad', 'Rice', 'Pasta', 'Vegetables', 'DummyC'],
        'type': 'category'
    }
    data['objects'].append(category)

    # Init
    data['init'].append({'name': 'incompatible', 'random': True, 'args': 2, 'types': [main_course, second_course]})
    data['init'].append({'name': 'classified', 'random': False, 'values': generate_classifications(
        main_course['values'], second_course['values'], category['values']
    )})
    data['init'].append({'name': 'dayBefore', 'random': False, 'values': generate_day_before(day['values'])})
    data['init'].append({'name': 'servedOnly', 'random': True, 'args': 2, 'types': [dish, day]})
    data['init'].append({'name': 'calories', 'random': False, 'values': generate_calories(
        main_course['values'], second_course['values'], 1000, 1500
    )})
    data['init'].append({'name': 'prices', 'random': False, 'values': generate_prices(
        main_course['values'], second_course['values']
    )})

    # Create goal
    goal = '(:goal\n' + 4 * ' ' + '(forall (?d - day)\n' + 6 * ' ' + '(and (mainReady ?d) (secondReady ?d))\n' + 4 * ' ' + ')\n' + 2 * ' ' + ')'
    goal += '\n' + 2 * ' ' + '(:metric minimize (totalPrice))'

    # Create objects
    objects = ''
    for obj in data['objects']:
        objects += 4 * ' ' + ' '.join(obj['values']) + ' - ' + obj['type'] + '\n'
    objects = objects[:-1]

    # Create init
    init = ''
    for pred in data['init']:
        if pred['random']:
            max_range = 5
            if pred['name'] == 'incompatible':
                max_range = 10
            for _ in range(random.randint(1, max_range)):
                init += 4 * ' ' + generate_predicate(pred) + '\n'
            init += '\n'
        else:
            init += pred['values']
    init = init[:-2]

    file_tpl = os.path.join('templates', 'problem.tpl')
    with open(file_tpl, 'r') as f:
        template = f.read()
        template = template.format(problem='ricoRico', domain='ricoRico', objects=objects, init=init, goal=goal)
        return template

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes PDDL RicoRico extension_5')
    parser.add_argument('tests', metavar='tests', type=int, help='Number of tests')

    args = parser.parse_args()
    n_tests = args.tests

    test_path = os.path.join('extension_5')
    test_files = [f for f in os.listdir(test_path) if os.path.isfile(os.path.join(test_path, f)) and '_ts_' in f]
    min_test = 0
    if len(test_files) != 0:
        answer_ok = False
        while not answer_ok:
            delete_files = input("Detected some existing test suites, do you want to remove them? If not, new ones will be added [Y/N]: ")
            if delete_files.lower() in ['y', 'yes', 'ok', 'accept']:
                for f in test_files:
                    os.remove(os.path.join(test_path, f))
                answer_ok = True
            elif delete_files.lower() in ['n', 'no', 'deny', 'cancel']:
                min_test = len(test_files)
                answer_ok = True
            else:
                print('Sorry but I can\'t understand your answer')

    for n in range(n_tests):
        test = generate_test()
        test_file = os.path.join('extension_5', 'rico_rico_ts_' + str(min_test + n) + '.pddl')
        with open(test_file, "w") as wf:
            wf.write(test)