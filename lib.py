import json
import os
import glob
import math


def get_file_data(filename):
    lines_count = 0
    characters_count = 0

    with open(filename) as f:
        for i, line in enumerate(f):
            line = line.strip()  # Ignore whitespaces

            if line == "": continue  # Do not count empty lines

            lines_count += 1
            characters_count += len(line)

    return lines_count, characters_count


class Serializable:
    """Class to configure JSON output"""

    def toJSON(self):
        return self.__dict__


class ExtensionEntry(Serializable):
    """Class to represent analysis data of an extension"""

    CHARACTERS_PER_LINE = 60  # TODO brauchen beleg

    def __init__(self, extension):
        self.extension = extension
        self.characters = 0
        self.files_count = 0
        self.lines_count = 0
        self.normalizedLines = 0

    def add_file_data(self, filename):
        self.files_count += 1
        lines_count, chars_count = get_file_data(filename)
        self.characters += chars_count
        self.lines_count += lines_count

    def analyze(self):
        self.normalizedLines = self.characters / self.CHARACTERS_PER_LINE
        self.normalizedLines = math.ceil(self.normalizedLines)


class ExtensionEntriesDictionary(Serializable):
    """Class to represent dictionary of all ExtensionEntries"""

    def __init__(self):
        self.extensions_count = 0
        self.entries = {}

    def get_entry(self, file_extension):
        if file_extension in self.entries:
            current_entry = self.entries[file_extension]
        else:
            current_entry = ExtensionEntry(file_extension)
            self.entries[file_extension] = current_entry
            self.extensions_count += 1
        return current_entry

class AnalysisData(Serializable):
    """Class to represent all data of analysis"""

    def __init__(self):
        self.entries_dict = ExtensionEntriesDictionary()
        self.files_without_extension = 0

    def write_output_to_file(self, output_file_path):
        json_output = json.dumps(self, default=lambda object: object.toJSON(), indent=4)
        f = open(output_file_path, "w")
        f.write(json_output)
        f.close()


class Analyzer:
    """Class where the actual analysis takes place"""

    def __init__(self, input_dir, output_file):
        self.input_dir = os.path.abspath(input_dir)
        self.output_file = os.path.abspath(output_file)

    def analyze_dir(self, detailed_output):
        if detailed_output: print("\nAnalyzing directory " + self.input_dir + "\n\n")

        analysis_data = AnalysisData()
        extension_entries_dict = analysis_data.entries_dict

        # Loop through files

        for filename in glob.glob(self.input_dir + "/**/*", recursive=True):
            if detailed_output: print(filename)
            if not os.path.isfile(filename): continue  # Skip directories

            # Get entry for filename

            file_extension = os.path.splitext(filename)[1]  # TODO brauchen z.B. .blade.php einzeln von .php?
            if file_extension == "":
                analysis_data.files_without_extension += 1
                continue

            current_entry = extension_entries_dict.get_entry(file_extension)
            current_entry.add_file_data(filename)

        self.analyze_entries(extension_entries_dict)

        analysis_data.write_output_to_file(self.output_file)

    def analyze_entries(self, extension_entries_dict):
        for key, entry in extension_entries_dict.entries.items():
            entry.analyze()