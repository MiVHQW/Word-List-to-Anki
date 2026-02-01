import re

import duden


class Word:
    """Represents a word from the duden."""

    def __init__(self, word_string: str):
        """Instantiates the word and fetches it from the duden.
        :type word_string: str
        """

        self.word_string = word_string.strip()
        self.word = duden.get(self.word_to_url_friendly_word(self.word_string))

    def word_to_url_friendly_word(self, word: str):
        string = word.strip()

        replace_dict = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "sz", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"}

        for k in replace_dict.keys():
            string = string.replace(k, replace_dict[k])
        return string

    def hide_word_in_text(self, text: str):
        """Replaces all occurences of 'word' in text with '~'."""

        replacement = "~"
        result_text = text.replace(self.word_string, replacement)

        if self.word_string.endswith("en") and len(self.word_string) > 5:
            result_text = text.replace(self.word_string[:-2], replacement)

        return result_text

    @staticmethod
    def return_with_paragraph_at_end(input_string: str):
        return input_string + "<br>"

    @staticmethod
    def remove_trailing_str(trailing_chars: str, base_string: str):

        index_of_right_string = base_string.rfind(trailing_chars)
        if index_of_right_string == len(base_string) - len(trailing_chars):
            result = base_string[:index_of_right_string]
        else:
            result = base_string

        return result

    def remove_herkunft(self, input_string: str):
        index_of_right_string = input_string.rfind("Herkunft")
        if index_of_right_string != -1:
            result = input_string[:index_of_right_string]
            result = self.remove_trailing_str("<br>", result)
            result = self.remove_trailing_str("\n", result)
        else:
            return input_string

        return result

    def export_string_for_anki(self):
        """Generates a string with the title separated by tab from the meaning"""
        export_string = ""

        if type(self.word.meaning_overview) == list:  # several meanings
            for meaning in self.word.meaning_overview:
                if type(meaning) == str:  # when normal string, just print

                    export_string += self.return_with_paragraph_at_end(meaning)

                elif type(meaning) == list:  # a list in itself, so iterate again
                    for submeaning in meaning:
                        export_string += self.return_with_paragraph_at_end(submeaning)

                else:
                    raise TypeError("Unknown Type")

        if type(self.word.meaning_overview) == str:  # one meaning
            export_string += self.word.meaning_overview

        # remove herkunft
        export_string = self.remove_herkunft(export_string)

        # remove trailing to get equal starting point for examples
        export_string = self.remove_trailing_str("<br>", export_string)

        # add examples
        examples = self.word.examples
        examples = self.hide_word_in_text(examples)
        if examples:
            export_string += "<br><br>Beispiel<br>"
            export_string += examples.replace("\n", "<br>")

        # remove tabs in meaning in order to not confuse anki
        # on import
        export_string = re.sub("\t", "", export_string)

        # remove trailing paragraph
        export_string = self.remove_trailing_str("<br>", export_string)

        # create output string with title and export string
        result = self.word.title + "\t" + '"' + export_string + '"'

        return result
