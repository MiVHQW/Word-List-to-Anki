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

    def txt_to_search_string_list(self, path):
        """
        Reads a txt file with one search string per line and
        creates a python list with one str per line

        :type path: str
        """
        with open(path, "r", encoding="UTF-8") as f:
            search_strings = f.readlines()

        return search_strings

    def word_string_to_word_object(self, word_string):
        return Word(word_string)

    def create_word_list(self):
        # read txt and create word string list
        word_string_list = self.txt_to_search_string_list(
            r"Input/words.txt")

        # create word objects

        for word_string in word_string_list:
            self.word_objects.append(self.word_string_to_word_object(word_string))
            try:
                print(self.word_string_to_word_object(word_string).word.title, ": success", sep="")

                string_to_be_added = (self.word_string_to_word_object(word_string).export_string_for_anki() + "\n")

                # add string
                self.export_words += string_to_be_added



            except:
                print(self.word_string_to_word_object(word_string).word_string, ": failed", sep="")
                self.error_words += (self.word_string_to_word_object(word_string).word_string + "\n")

        # remove newlines before " in the ok words string
        export_words = re.sub('\n"', '"', self.export_words)

        # write export file
        with open(self.ok_list_path, "w", encoding="utf8") as f:
            f.write(export_words)

        # write error file
        with open(self.error_list_path, "w", encoding="utf8") as f:
            f.write(self.error_words)

        input("You can close this window now.")


my_factory = WordFactory(r"Input/words.txt")
my_factory.create_word_list()
