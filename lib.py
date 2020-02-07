import json

class Serializable:

    def toJSON(self):
        return self.__dict__


class ExtensionEntry(Serializable):
    CHARACTERS_PER_LINE = 60  # TODO brauchen beleg

    def __init__(self, extension):
        self.extension = extension
        self.characters = 0
        self.files_count = 0

    def add_file_data(self, filename):
        self.files_count += 1


class ExtensionEntriesDictionary(Serializable):

    def __init__(self):
        self.extensions_count = 0
        self.entries = {}

    def get_entry(self, file_extension):
        if file_extension in self.entries:
            current_entry = self.entries[file_extension]
        else:
            current_entry = ExtensionEntry(file_extension)
            self.entries[file_extension] = current_entry
            self.extensions_count +=1
        return current_entry


class AnalysisData(Serializable):

    def __init__(self):
        self.entries_dict = ExtensionEntriesDictionary()
        self.files_without_extension = 0

    def write_output_to_file(self, output_file_path):
        json_output = json.dumps(self, default=lambda object: object.toJSON(), indent=4)
        f = open(output_file_path, "w")
        f.write(json_output)
        f.close()
