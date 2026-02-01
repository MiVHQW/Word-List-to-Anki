import re

from Word_Class import Word


class WordFactory:
    """Converts an input list into an output file for Anki to import."""

    def __init__(self, input_file_path: str):
        self.input_file_path = input_file_path
        self.ok_list_path = "Output/export_words.txt"
        self.error_list_path = "Output/error_words.txt"
        self.word_objects = []
        self.export_words = ""
        self.error_words = ""

    @staticmethod
    def txt_file_to_string_list(path):
        """
        Reads a txt file with one search string per line and
        creates a python list

        :type path: str
        """
        with open(path, "r", encoding="UTF-8") as f:
            search_strings = f.readlines()

        return search_strings

    @staticmethod
    def word_string_to_word_object(word_string):
        """Creates word objects from strings"""
        return Word(word_string)

    def createWordObjectList(self):
        # read txt and create word string list
        word_string_list = self.txt_file_to_string_list(
            r"Input/words.txt")

        # create word objects

        for word_string in word_string_list:
            try:
                word_object = self.word_string_to_word_object(word_string)
                self.word_objects.append(self.word_string_to_word_object(word_string))

            except:
                print(word_string, ": failed", sep="")
                self.error_words += word_string + "\n"
                continue

            title = word_object.word.title
            print(title, ": success", sep="")

    def write_to_file(self):
        # write export file
        with open(self.ok_list_path, "w", encoding="utf8") as f:
            f.write(self.export_words)

        # write error file
        with open(self.error_list_path, "w", encoding="utf8") as f:
            f.write(self.error_words)

        input("You can close this window now.")

    def create_output_file(self):
        """Creates the Anki output file
        """
        self.createWordObjectList()

        for word_object in self.word_objects:
            string_to_be_added = word_object.export_string_for_anki()

            # add string
            self.export_words += (string_to_be_added + "\n")

            # remove newlines before " in the ok words string
            self.export_words = re.sub('\n"', '"', self.export_words)

        self.write_to_file()


my_factory = WordFactory(r"Input/words.txt")
my_factory.create_output_file()
