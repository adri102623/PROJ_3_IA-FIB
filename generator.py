import argparse
import os
import random

def generar_test():
    def generar_predicado(genpred):
        argumentos = genpred['args']
        predicado = '(' + genpred['name']
        for arg in range(argumentos):
            predicado += ' ' + random.choice(genpred['types'][arg]['values'])
        return predicado + ')'

    def generar_day_before(dias):
        day_before = ''
        for i in range(len(dias) - 1):
            day_before += 4 * ' ' + '(dayBefore ' + dias[i] + ' ' + dias[i + 1] + ')\n'
        day_before += '\n' + 4 * ' ' + '(mainReady DummyD)'
        day_before += '\n' + 4 * ' ' + '(secondReady DummyD)'
        day_before += '\n' + 4 * ' ' + '(dayMCClassif DummyD DummyC)'
        return day_before + '\n' + 4 * ' ' + '(daySCClassif DummyD DummyC)\n\n'

    def generar_clasificaciones(primeros, segundos, categorias):
        categorias_mc = [5, 3, 6, 4, 6, 0, 1, 6, 2, 2, 2, 0, 4]
        categorias_sc = [1, 1, 4, 0, 1, 1, 6, 1, 6, 5, 5, 0]

        clasificacion = ''
        for index, plato in enumerate(primeros):
            clasificacion += 4 * ' ' + '(classified ' + plato + ' ' + categorias[categorias_mc[index]] + ')\n'
        for index, plato in enumerate(segundos):
            clasificacion += 4 * ' ' + '(classified ' + plato + ' ' + categorias[categorias_sc[index]] + ')\n'
        return clasificacion + '\n'

    def generar_calorias(primeros, segundos, min_calorias, max_calorias):
        calorias_primeros = [500, 120, 290, 490, 610, 720, 1000, 240, 600, 760, 480, 320, 410]
        calorias_segundos = [810, 380, 700, 670, 520, 490, 250, 960, 320, 480, 430, 750]

        calorias = 4 * ' ' + '(= (minCalories) ' + str(min_calorias) + ')\n' + 4 * ' ' + '(= (maxCalories) ' + str(max_calorias) + ')\n\n'
        for index, plato in enumerate(primeros):
            calorias += 4 * ' ' + '(= (calories ' + plato + ') ' + str(calorias_primeros[index]) + ')\n'
        for index, plato in enumerate(segundos):
            calorias += 4 * ' ' + '(= (calories ' + plato + ') ' + str(calorias_segundos[index]) + ')\n'
        return calorias + '\n'

    def generar_precios(primeros, segundos):
        precios_primeros = [8, 7, 5, 12, 10, 15, 5, 10, 16, 9, 11, 6, 13]
        precios_segundos = [17, 4, 25, 20, 14, 19, 9, 21, 12, 6, 6, 13]

        precios = 4 * ' ' + '(= (totalPrice) 0)\n\n'
        for index, plato in enumerate(primeros):
            precios += 4 * ' ' + '(= (price ' + plato + ') ' + str(precios_primeros[index]) + ')\n'
        for index, plato in enumerate(segundos):
            precios += 4 * ' ' + '(= (price ' + plato + ') ' + str(precios_segundos[index]) + ')\n'
        return precios + '\n'

    datos = {
        'objects': [],
        'init': [],
        'goal': []
    }

    # Objetos
    dia = {
        'values': ['DummyD', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'type': 'day'
    }
    datos['objects'].append(dia)

    primer_plato = {
        'values': ['Spaghetti_Bolognese', 'Mediterranean_Salad', 'Vegan_Sandwich', 'Mushroom_risotto',
                   'Guacamole_with_tomatoes', 'Sushi', 'American_burger', 'Broccoli_quiche',
                   'Kirmizi_Mercimek_Corbasi', 'Chinese_Noodles_With_Vegetables', 'Chana_masala',
                   'Chinese_tiger_salad', 'Shumai'],
        'type': 'mainCourse'
    }
    datos['objects'].append(primer_plato)

    segundo_plato = {
        'values': ['Roast_pork_with_prunes', 'Spanish_omelette', 'Paella', 'Tuna_steak', 'Chicken_parmesan',
                   'Lamb_tagine', 'Couscous_meatloaf', 'Coq_au_vin', 'Mapo_tofu', 'Persian_pie', 'Burrito_pie',
                   'Spicy_seafood_stew'],
        'type': 'secondCourse'
    }
    datos['objects'].append(segundo_plato)

    plato = {
        'values': primer_plato['values'] + segundo_plato['values'],
        'type': 'dish'
    }

    categoria = {
        'values': ['Fish', 'Meat', 'Soup', 'Salad', 'Rice', 'Pasta', 'Vegetables', 'DummyC'],
        'type': 'category'
    }
    datos['objects'].append(categoria)

    # Init
    datos['init'].append({'name': 'incompatible', 'random': True, 'args': 2, 'types': [primer_plato, segundo_plato]})
    datos['init'].append({'name': 'classified', 'random': False, 'values': generar_clasificaciones(
        primer_plato['values'], segundo_plato['values'], categoria['values']
    )})
    datos['init'].append({'name': 'dayBefore', 'random': False, 'values': generar_day_before(dia['values'])})
    datos['init'].append({'name': 'servedOnly', 'random': True, 'args': 2, 'types': [plato, dia]})
    datos['init'].append({'name': 'calories', 'random': False, 'values': generar_calorias(
        primer_plato['values'], segundo_plato['values'], 1000, 1500
    )})
    datos['init'].append({'name': 'prices', 'random': False, 'values': generar_precios(
        primer_plato['values'], segundo_plato['values']
    )})

    # Crear goal
    goal = '(:goal\n' + 4 * ' ' + '(forall (?d - day)\n' + 6 * ' ' + '(and (mainReady ?d) (secondReady ?d))\n' + 4 * ' ' + ')\n' + 2 * ' ' + ')'
    goal += '\n' + 2 * ' ' + '(:metric minimize (totalPrice))'

    # Crear objects
    objects = ''
    for obj in datos['objects']:
        objects += 4 * ' ' + ' '.join(obj['values']) + ' - ' + obj['type'] + '\n'
    objects = objects[:-1]

    # Crear init
    init = ''
    for pred in datos['init']:
        if pred['random']:
            max_range = 5
            if pred['name'] == 'incompatible':
                max_range = 10
            for _ in range(random.randint(1, max_range)):
                init += 4 * ' ' + generar_predicado(pred) + '\n'
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
    parser = argparse.ArgumentParser(description='Ejecuta el generador de problemas PDDL para RicoRico extension_5')
    parser.add_argument('tests', metavar='tests', type=int, help='Número de tests a generar')

    args = parser.parse_args()
    n_tests = args.tests

    test_path = os.path.join('extension_5')
    test_files = [f for f in os.listdir(test_path) if os.path.isfile(os.path.join(test_path, f)) and '_ts_' in f]
    min_test = 0
    if len(test_files) != 0:
        answer_ok = False
        while not answer_ok:
            delete_files = input("Se han detectado tests existentes, ¿quieres eliminarlos? Si no, se añadirán nuevos. [Y/N]: ")
            if delete_files.lower() in ['y', 'yes', 'ok', 'accept', 's', 'si']:
                for f in test_files:
                    os.remove(os.path.join(test_path, f))
                answer_ok = True
            elif delete_files.lower() in ['n', 'no', 'deny', 'cancel']:
                min_test = len(test_files)
                answer_ok = True
            else:
                print('No he entendido tu respuesta.')

    for n in range(n_tests):
        test = generar_test()
        test_file = os.path.join('extension_5', 'rico_rico_ts_' + str(min_test + n) + '.pddl')
        with open(test_file, "w") as wf:
            wf.write(test)