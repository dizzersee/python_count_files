import glob
import os
import json
from lib import ExtensionEntriesDictionary
from lib import AnalysisData
import lib

# TODO read values in
dir_path = "./analyzedDir"  # This will be user input
output_file_path = "output.json"  # this will be output

abs_dir_path = os.path.abspath(dir_path)
print("\nAnalyzing directory " + abs_dir_path + "\n\n")

analysisData = AnalysisData()
extension_entries_dict = analysisData.entries_dict

# Loop through files

for filename in glob.glob(abs_dir_path + "/**/*", recursive=True):
    print(filename)
    if not os.path.isfile(filename): continue  # Skip directories

    # Get entry for filename

    file_extension = os.path.splitext(filename)[1]  # TODO brauchen z.B. .blade.php einzeln von .php?
    if file_extension == "":  # todo test if works
        analysisData.files_without_extension += 1
        continue  # todo add this to json output

    currentEntry = extension_entries_dict.get_entry(file_extension)
    currentEntry.add_file_data(filename)

analysisData.write_output_to_file(output_file_path)
