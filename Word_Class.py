import duden
import re


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

    def decorator_func(self, meaning, submeaning=False):
        def printer(multiplier):
            print(meaning, end="<br>" * multiplier)

        if submeaning == False:
            printer(2)

        if submeaning:
            printer(1)

    def print_for_anki(self):
        """prints word and meaning with separation"""
        print(self.word.title, "\n")

        if type(self.word.meaning_overview) == list:  # several meanings
            for meaning in self.word.meaning_overview:
                if type(meaning) == str:  # when normal string, just print

                    self.decorator_func(meaning)
                elif type(meaning) == list:  # a list in itself, so iterate again
                    for submeaning in meaning:
                        self.decorator_func(submeaning, submeaning=True)
                else:
                    raise TypeError("Unknown Type")

        if type(self.word.meaning_overview) == str:  # one meaning
            self.decorator_func(self.word.meaning_overview)

    def export_string_for_anki(self):
        """Generates a string with the title separated by tab from the meaning"""
        export_string = ""

        def remove_trailing_str(trailing_chars: str, base_string: str):
            index_of_right_string = base_string.rfind(trailing_chars)

            if index_of_right_string == -1:
                without = base_string
            else:
                without = base_string[:index_of_right_string]

            return without

        if type(self.word.meaning_overview) == list:  # several meanings
            for meaning in self.word.meaning_overview:
                if type(meaning) == str:  # when normal string, just print

                    export_string += (meaning + "<br>")

                elif type(meaning) == list:  # a list in itself, so iterate again
                    for submeaning in meaning:
                        export_string += submeaning + "<br>"

                else:
                    raise TypeError("Unknown Type")

        if type(self.word.meaning_overview) == str:  # one meaning
            export_string += (self.word.meaning_overview)

        # remove tabs in meaning in order to not confuse anki
        # on import
        export_string = re.sub("\t", "", export_string)

        # remove trailing whitespace
        export_string = remove_trailing_str("<br>", export_string)

        result = self.word.title + "\t" + '"' + export_string + '"'
        return result

    def print_synonyms(self):
        try:
            print(duden.get(self.word.synonyms))
        except:
            print("No synonyms.")
