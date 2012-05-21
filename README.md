def
===
A dictionary with a command-line interface using Google Dictionary's
(unofficial) definitions in JSON.

Setup
-----
### Manual install (Linux & Mac)
Open a terminal and paste the following commands into it:

    git clone git://github.com/haukurpallh/def.git
    mv def/ ~/.def
    chmod +x ~/.def/define.py
    sudo ln -s ~/.def/define.py /usr/bin/def

Usage
-----
Open a terminal and type `def word`. It should print the following:

        Word
    Noun
      • A single distinct meaningful element of speech or writing, used with
        others (or sometimes alone) to form a sentence and typically shown with
        a space on either side when written or printed.
      • A single distinct conceptual unit of language, comprising inflected and
        variant forms.
      • Something that someone says or writes; a remark or piece of
        information.
    Verb
      • Choose and use particular words in order to say or write (something).
    Exclamation
      • Used to express agreement.

For help you can type `def -h`.
