import re

from duden_word_fetcher import Word


def txt_to_search_string_list(path):
    """
    Reads a txt file with one search string per line and
    creates a python list with one str per line

    :type path: str
    """
    with open(path, "r", encoding="UTF-8") as f:
        search_strings = f.readlines()

    return search_strings


def word_string_to_word_object(word_string):
    return Word(word_string)


# read txt and create word string list
word_string_list = txt_to_search_string_list(
    r"words.txt")
ok_list_path = "export_words.txt"
error_list_path = "error_words.txt"
export_words = ""
error_words = ""

# create word objects
word_objects = []
for word_string in word_string_list:
    word_objects.append(word_string_to_word_object(word_string))
    try:
        print(word_string_to_word_object(word_string).word.title, ": success", sep="")

        string_to_be_added = (word_string_to_word_object(word_string).export_string_for_anki() + "\n")

        # add string
        export_words += string_to_be_added



    except:
        print(word_string_to_word_object(word_string).word_string, ": failed", sep="")
        error_words += (word_string_to_word_object(word_string).word_string + "\n")

# remove newlines before " in the ok words string
export_words = re.sub('\n"', '"', export_words)

# write export file
with open(ok_list_path, "w", encoding="utf8") as f:
    f.write(export_words)

# write error file
with open(error_list_path, "w", encoding="utf8") as f:
    f.write(error_words)
