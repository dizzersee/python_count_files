import json


class ExtensionEntry:
    characters = 0
    files_count = 0
    CHARACTERS_PER_LINE = 60  # TODO brauchen beleg

    def __init__(self, extension):
        self.extension = extension

    def toJSON(self):
        return self.__dict__


class ExtensionEntriesDictionary:

    def __init__(self):
        self.entries = {}

    def get_entry(self, file_extension):
        if file_extension in self.entries:
            current_entry = self.entries[file_extension]
        else:
            current_entry = ExtensionEntry(file_extension)
            self.entries[file_extension] = current_entry
        return current_entry

    def write_output_to_file(self, output_file_path):
        json_output = json.dumps(self.entries, default=lambda object: object.toJSON(), indent=4)
        f = open(output_file_path, "w")
        f.write(json_output)
        f.close()


