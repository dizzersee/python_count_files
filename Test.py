import glob
import os
import json
from lib import ExtensionEntriesDictionary
import lib

# TODO read values in
dir_path = "./analyzedDir"  # This will be user input
output_file_path = "output.json"  # this will be output

abs_dir_path = os.path.abspath(dir_path)
print("\nAnalyzing directory " + abs_dir_path + "\n\n")

extension_entries_dict = ExtensionEntriesDictionary()

for filename in glob.glob(abs_dir_path + "/**/*", recursive=True):
    print(filename)
    if not os.path.isfile(filename): continue  # Skip directories
    file_extension = os.path.splitext(filename)[1]
    currentEntry = extension_entries_dict.get_entry(file_extension)
    currentEntry.files_count += 1

extension_entries_dict.write_output_to_file(output_file_path)

