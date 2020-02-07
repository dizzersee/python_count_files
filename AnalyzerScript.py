from lib import Analyzer

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--input-dir", dest="input_dir", help="Input directory path")
parser.add_argument("-o", "--output-file", dest="output_file", help="Output file path")
parser.add_argument("-v", "--verbose", dest="verbose", help="Detailed output")

args = parser.parse_args()
if args.input_dir is None or args.output_file is None :
    print("Please provide input dir path with -i")
    print("Please provide output file path with -o")
    exit()

dir_path = args.input_dir
output_file_path = args.output_file
verbose = args.verbose is not None

analyzer = Analyzer(dir_path, output_file_path)
analyzer.analyze_dir(verbose)