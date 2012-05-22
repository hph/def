def
===
A dictionary with a command-line interface using Google Dictionary's
(unofficial) definitions in JSON. See
[Usage examples](https://github.com/haukurpallh/def#usage-examples) for an
overview of the features.
![Screenshot](http://i.imgur.com/0MJjr.png)

Setup
-----
### Manual install (Linux & Mac)
Open a terminal and paste the following commands into it:

    git clone git://github.com/haukurpallh/def.git
    mv def/ ~/.def
    chmod +x ~/.def/define.py
    sudo ln -s ~/.def/define.py /usr/bin/def

Usage examples
--------------
### Basic usage
Open a terminal and type `def word`. It should print the following:

        word  ―  /wərd/
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

### Slightly more advanced features
For a full list of features type `def -h`.

The `-n` option allows you to specify the number of definitions (for each
category) that you want to print. For example, `def -n=1 horse` will give you:

        horse  ―  /hôrs/
    Noun
      • A solid-hoofed plant-eating domesticated mammal with a flowing mane and
        tail, used for riding, racing, and to carry and pull loads
    Verb
      • Provide (a person or vehicle) with a horse or horses

On the other hand, `def -n=5 horse` will print:

        horse  ―  /hôrs/
    Noun
      • A solid-hoofed plant-eating domesticated mammal with a flowing mane and
        tail, used for riding, racing, and to carry and pull loads
      • An adult male horse; a stallion or gelding
      • A wild mammal of the horse family
      • Cavalry
      • A frame or structure on which something is mounted or supported, esp. a
        sawhorse
    Verb
      • Provide (a person or vehicle) with a horse or horses

The `-b` option allows you to specify which bullet type you want. The default,
as seen above, is `•`. `d` stands for `dash`:

    def -b=d music

Which will print:

        mu·sic  ―  /ˈmyo͞ozik/
    Noun
      ― The art or science of combining vocal or instrumental sounds (or both)
        to produce beauty of form, harmony, and expression of emotion
      ― The vocal or instrumental sound produced in this way
      ― A sound perceived as pleasingly harmonious

For a triangular bullet, use `t` (triangle):

    def -b=t music

Which prints:

        mu·sic  ―  /ˈmyo͞ozik/
    Noun
      ‣ The art or science of combining vocal or instrumental sounds (or both)
        to produce beauty of form, harmony, and expression of emotion
      ‣ The vocal or instrumental sound produced in this way
      ‣ A sound perceived as pleasingly harmonious

And finally, for an empty bullet, use `w` (white).

    def -b=w music

Which prints:

        mu·sic  ―  /ˈmyo͞ozik/
    Noun
      ◦ The art or science of combining vocal or instrumental sounds (or both)
        to produce beauty of form, harmony, and expression of emotion
      ◦ The vocal or instrumental sound produced in this way
      ◦ A sound perceived as pleasingly harmonious

There may be times when you want to save the output of the program in a file.
On Linux and Mac you can do that by typing `def word > file.txt`. This saves
the output of `def word` in `file.txt` in the current folder. However, it would
be better to do `def -q word > file.txt` since you probably wouldn't want error
messages saved. That's what the `-q` or `--quiet` option is for.

If you dislike the default behaviour you don't need to type all the options.
Simply create an alias in your `.bashrc` (located in your home folder). For
example, if you'd like def to print five definitions for each category instead
of the default of three, you could add the following line to your `.bashrc`:

    alias def='def n=5'

And now, if you type `def word` it prints:

        word  ―  /wərd/
    Noun
      • A single distinct meaningful element of speech or writing, used with
        others (or sometimes alone) to form a sentence and typically shown with
        a space on either side when written or printed
      • A single distinct conceptual unit of language, comprising inflected and
        variant forms
      • Something that someone says or writes; a remark or piece of information
      • Speech as distinct from action
      • Even the smallest amount of something spoken or written
    Verb
      • Choose and use particular words in order to say or write (something)
    Exclamation
      • Used to express agreement

Future features
---------------
- Multiple language support
- Option to parse a file and create a file with all the definitions
- Option to get more than one definition at a time
- Option to get only one definition from one category or only definitions from
  one category
- Usage example beneath definitions
- Installer and updater
- Man page (so that a readme is available via `man def`)
- Web definitions or other sources for words that can't be found
- Any suggestions are welcome

Notes
-----
Don't hesitate to report bugs at: https://github.com/haukurpallh/def/issues
