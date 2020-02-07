import unittest
from lib import Analyzer
import os
import shutil
import json


class AnalyzerTest(unittest.TestCase):
    PHP_CHARS_PER_LINE = 33
    PHP_LINES_PER_FILE = 5
    TEST_DIR_NAME = "./testdir"
    TEST_SUB_DIR_NAME = "subdir"
    OUTPUT_FILE_NAME = "./test_out.json"

    def setUp(self) -> None:
        if not os.path.exists(self.TEST_DIR_NAME):
            os.mkdir(self.TEST_DIR_NAME)

        if not os.path.exists(self.TEST_DIR_NAME + self.TEST_SUB_DIR_NAME):
            os.mkdir(self.TEST_DIR_NAME + "/" + self.TEST_SUB_DIR_NAME)

    def tearDown(self) -> None:
        shutil.rmtree(self.TEST_DIR_NAME)
       # os.remove(self.OUTPUT_FILE_NAME)

    def test_output(self):
        file1 = ((self.PHP_CHARS_PER_LINE * 'a') + '\n') * self.PHP_LINES_PER_FILE
        self.write_to_file(self.TEST_DIR_NAME + "/" + "test.blade.php", file1)

        file2 = "111111\n\n222"
        self.write_to_file(self.TEST_DIR_NAME + "/" + self.TEST_SUB_DIR_NAME + "/test.js", file2)

        self.write_to_file(self.TEST_DIR_NAME + "/" + "noext", "test")

        analyzer = Analyzer(self.TEST_DIR_NAME, self.OUTPUT_FILE_NAME)
        analyzer.analyze_dir(False)

        f = open(self.OUTPUT_FILE_NAME, "r")
        obj = json.loads(f.read())
        f.close()
        i = 5
        self.assertEqual(obj['entries_dict']['extensions_count'], 2)
        self.assertEqual(obj['files_without_extension'], 1)

        php_entry = obj['entries_dict']['entries']['blade.php']
        self.assertEqual(php_entry['extension'], 'blade.php')
        self.assertEqual(php_entry['total_characters'], self.PHP_CHARS_PER_LINE * self.PHP_LINES_PER_FILE)
        self.assertEqual(php_entry['total_files_count'], 1)
        self.assertEqual(php_entry['total_lines_count'], self.PHP_LINES_PER_FILE)
        self.assertEqual(php_entry['total_normalized_lines'], 3)

        js_entry = obj['entries_dict']['entries']['js']
        self.assertEqual(js_entry['extension'], 'js')
        self.assertEqual(js_entry['total_characters'], 9)
        self.assertEqual(js_entry['total_files_count'], 1)
        self.assertEqual(js_entry['total_lines_count'], 2)
        self.assertEqual(js_entry['total_normalized_lines'], 1)


    def write_to_file(self, filepath, content):
        f = open(filepath, 'w+')
        f.write(content)
        f.close()
