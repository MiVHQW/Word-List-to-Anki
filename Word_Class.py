import re

import duden


class Word:
    """Represents a word from the duden."""

    def __init__(self, word_string):
        """Instantiates the word and fetches it from the duden.
        :type word_string: str
        """

        def word_to_url_friendly_word(word):
            string = word.strip()

            replace_dict = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "sz", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"}

            for k in replace_dict.keys():
                string = string.replace(k, replace_dict[k])
            return string

        self.word_string = word_string
        self.word = duden.get(word_to_url_friendly_word(word_string))

    def hide_word_in_text(self, text: str):
        """Replaces all occurences of 'word' in text with '~'."""

        replacement = "~"
        result_text = text.replace(self.word_string, replacement)

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

        # add examples
        examples = self.word.examples
        examples = self.hide_word_in_text(examples)
        if examples:
            export_string += "<br>Beispiel<br>"
            export_string += examples.replace("\n", "<br>")

        # remove tabs in meaning in order to not confuse anki
        # on import
        export_string = re.sub("\t", "", export_string)

        # remove trailing paragraph
        export_string = self.remove_trailing_str("<br>", export_string)

        # create output string with title and export string
        result = self.word.title + "\t" + '"' + export_string + '"'

        return result
