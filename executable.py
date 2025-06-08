import argparse
import os
import platform
import sys

def print_error():
    print('¡Solo disponible en Linux!')
    sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ejecuta el planificador PDDL RicoRico extension_5')
    parser.add_argument('--test', dest='test', action='store_const', const=True, default=False,
                        help='Ejecuta los tests')
    parser.add_argument('--ejemplos', dest='ejemplos', action='store_const', const=True, default=False,
                        help='Ejecuta los ejemplos')

    args = parser.parse_args()
    ejecutar_tests = args.test
    ejecutar_ejemplos = args.ejemplos

    # Solo soportamos Linux
    if platform.system() != 'Linux':
        print_error()

    ff_ejecutable = os.path.join('linux_metrics', 'ff') + ' -O'
    ruta_dominio = os.path.join('extension_5', 'rico_rico_domain.pddl')
    carpeta_version = os.path.join('extension_5')

    if ejecutar_tests:
        tests = [f for f in os.listdir(carpeta_version) if '_ts_' in f]
        for test in tests:
            ff_args = f' -o {ruta_dominio} -f {os.path.join(carpeta_version, test)}'
            print(f'//// EJECUTANDO TEST -> {test} ////')
            os.system(ff_ejecutable + ff_args)
    elif ejecutar_ejemplos:
        ejemplos = [f for f in os.listdir(carpeta_version) if '_ets_' in f]
        for ejemplo in ejemplos:
            ff_args = f' -o {ruta_dominio} -f {os.path.join(carpeta_version, ejemplo)}'
            print(f'//// EJECUTANDO EJEMPLO -> {ejemplo} ////')
            os.system(ff_ejecutable + ff_args)
    else:
        archivo_problema = os.path.join(carpeta_version, 'rico_rico.pddl')
        ff_args = f' -o {ruta_dominio} -f {archivo_problema}'
        print(f'Ejecutando -> {ff_ejecutable}{ff_args}')
        os.system(ff_ejecutable + ff_args)