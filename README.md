# Word-List-to-Anki

This software creates an importable file for the popular Anki flashcard software from a text file containing German
words.

By importing this file, Anki creates one note (card) per word.

The card consists of two sides: The word on one side and the meaning(s) on the other side of the card.

# Usage

1. Alter the file _words.txt_ in the root directory and **insert your words**. Insert **one word per line**.

2. **Execute** _word_list_to_anki.py_.

3. You find your exportable file as _export_words.txt_ in the root directory. You can import this file as a tab
   separated text file into Anki.

# Example

* Let's say you want to add the two German words _Kontrafaktur_ and _äquidistant_ into Anki.

* You enter these two words one per line into _words.txt_.

* After editing the file _words.txt_ the content looks like this:

```
Kontrafaktur
äquidistant
```

* Then you execute _word_list_to_anki.py_ and find the file _export_words.txt_
  in your root directory.

* You can import this file as a tab separated text file into Anki.

* Two cards will be created. E.g. the card for the word _äquidistant_ will look like this:

Side 1:

```
äquidistant
```

Side 2:

```
gleich weit entfernt, gleiche Abstände aufweisend (z. B. von Punkten oder Kurven)
```
