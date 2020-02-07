import glob
import os
from lib import Analyzer


# TODO read values in
dir_path = "./analyzedDir"  # This will be user input
output_file_path = "output.json"  # this will be output

analyzer = Analyzer(dir_path, output_file_path)
analyzer.analyze_dir(True)