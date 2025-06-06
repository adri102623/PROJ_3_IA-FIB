import argparse
import os
import platform
import sys

def print_error():
    print('Your OS is not currently supported!')
    sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes PDDL RicoRico extension_5')
    parser.add_argument('--test', dest='test', action='store_const', const=True, default=False,
                        help='Execute test suites')
    parser.add_argument('--examples', dest='examples', action='store_const', const=True, default=False,
                        help='Execute example test suites')

    args = parser.parse_args()
    executeTests = args.test
    executeExamples = args.examples

    # Només suportem Linux
    if platform.system() != 'Linux':
        print_error()

    ff_executable = os.path.join('linux_metrics', 'ff') + ' -O'
    domain_path = os.path.join('extension_5', 'rico_rico_domain.pddl')
    version_folder = os.path.join('extension_5')

    if executeTests:
        tests = [f for f in os.listdir(version_folder) if '_ts_' in f]
        for test in tests:
            ff_args = f' -o {domain_path} -f {os.path.join(version_folder, test)}'
            print(f'//// EXECUTING TEST -> {test} ////')
            os.system(ff_executable + ff_args)
    elif executeExamples:
        examples = [f for f in os.listdir(version_folder) if '_ets_' in f]
        for example in examples:
            ff_args = f' -o {domain_path} -f {os.path.join(version_folder, example)}'
            print(f'//// EXECUTING EXAMPLE TEST -> {example} ////')
            os.system(ff_executable + ff_args)
    else:
        file_problem = os.path.join(version_folder, 'rico_rico.pddl')
        ff_args = f' -o {domain_path} -f {file_problem}'
        print(f'Executing -> {ff_executable}{ff_args}')
        os.system(ff_executable + ff_args)