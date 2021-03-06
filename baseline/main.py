import argparse
import os
import sys

from mainA import test as testA
from mainA import train as trainA
from mainB import test as testB
from mainB import train as trainB
from mainC import test as testC
from mainC import train as trainC

OUTPUT_DIR_ABC = '../training/submit/scenario1-ABC'
OUTPUT_DIR_BC = '../training/submit/scenario2-BC'
OUTPUT_DIR_C = '../training/submit/scenario3-C'

INPUT_DIR = '../training/input'
TRAINING_DIR = '../training/gold'

INPUT_PREFIX = 'input_'
OUTPUT_A_PREFIX = 'output_A_'
OUTPUT_B_PREFIX = 'output_B_'
OUTPUT_C_PREFIX = 'output_C_'

def output_fname(input_fname, prefix, to_dir=None):
    dir_name = os.path.dirname(input_fname)
    fname = os.path.basename(input_fname)
    output = prefix + fname[len(INPUT_PREFIX):]
    if to_dir is not None:
        dir_name = to_dir
    return os.path.join(dir_name, output)

def process_file_ABC(input_fname, output_dir=OUTPUT_DIR_ABC):
    text_file = input_fname
    outputA = output_fname(text_file, OUTPUT_A_PREFIX, output_dir)
    outputB = output_fname(text_file, OUTPUT_B_PREFIX, output_dir)

    testA(text_file, output_dir)
    testB(text_file, outputA, output_dir)
    testC(text_file, outputA, outputB, output_dir)

def process_file_BC(input_fname, gold_fileA, output_dir=OUTPUT_DIR_BC):
    text_file = input_fname
    outputB = output_fname(text_file, OUTPUT_B_PREFIX, output_dir)

    testB(text_file, gold_fileA, output_dir)
    testC(text_file, gold_fileA, outputB, output_dir)

def process_file_C(input_fname, gold_fileA, gold_fileB, output_dir=OUTPUT_DIR_C):
    text_file = input_fname

    testC(text_file, gold_fileA, gold_fileB, output_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', nargs='?', default=INPUT_DIR, help='Process INPUT file')
    parser.add_argument('--test', action='store_true', help='Run on the test set')
    parser.add_argument('-t','--train', metavar='DIR', dest='train', default=TRAINING_DIR, action='store', help='Train from DIR directory')
    args = parser.parse_args(sys.argv[1:])

    if args.train:
        trainA(INPUT_DIR, args.train)
        trainB(INPUT_DIR, args.train)
        trainC(INPUT_DIR, args.train)

    if args.test:
        TEST_DIR = "../test/input/"
        SUBMIT_DIR = "../test/submit/"

        # Scenario 1
        input_fname = os.path.join(TEST_DIR, 'scenario1-ABC', 'input_scenario1.txt')
        process_file_ABC(input_fname, os.path.join(SUBMIT_DIR, 'scenario1-ABC'))

        # Scenario 2
        input_fname = os.path.join(TEST_DIR, 'scenario2-BC', 'input_scenario2.txt')
        gold_file_A = os.path.join(TEST_DIR, 'scenario2-BC', 'output_A_scenario2.txt')
        process_file_BC(input_fname, gold_file_A, os.path.join(SUBMIT_DIR, 'scenario2-BC'))

        # Scenario 3
        input_fname = os.path.join(TEST_DIR, 'scenario3-C', 'input_scenario3.txt')
        gold_file_A = os.path.join(TEST_DIR, 'scenario3-C', 'output_A_scenario3.txt')
        gold_file_B = os.path.join(TEST_DIR, 'scenario3-C', 'output_B_scenario3.txt')
        process_file_C(input_fname, gold_file_A, gold_file_B, os.path.join(SUBMIT_DIR, 'scenario3-C'))

        # gold_fileA = output_fname(input_fname, OUTPUT_A_PREFIX, TRAINING_DIR)
        # gold_fileB = output_fname(input_fname, OUTPUT_B_PREFIX, TRAINING_DIR)
        # process_file_BC(input_fname, gold_fileA)
        # process_file_C(input_fname, gold_fileA, gold_fileB)

    elif args.input:
        if os.path.isdir(args.input):
            for input_fname in os.listdir(args.input):
                input_fname = os.path.join(args.input, input_fname)
                process_file_ABC(input_fname)

                gold_fileA = output_fname(input_fname, OUTPUT_A_PREFIX, TRAINING_DIR)
                gold_fileB = output_fname(input_fname, OUTPUT_B_PREFIX, TRAINING_DIR)
                process_file_BC(input_fname, gold_fileA)
                process_file_C(input_fname, gold_fileA, gold_fileB)
        else:
            process_file_ABC(args.input)

if __name__ == '__main__':
    main()
