#!/usr/bin/python
#coding: utf8

from __future__ import division
from argparse import ArgumentParser
from ast import literal_eval
from math import ceil
from os import popen
from re import sub
from string import capitalize
from sys import argv, exit
from urllib import urlencode
from urllib2 import urlopen, URLError
from webbrowser import open as open_browser

def get_data(query, src_lan='en', tgt_lan='en', quiet=False):
    '''Return data in JSON from Google.''' 
    base_url = 'http://173.194.35.144/dictionary/json?callback=c&'
    options = urlencode({'q': query, 'sl': src_lan, 'tl': tgt_lan})
    try:
        return urlopen(base_url + options).read().decode('utf8')[2:-10]
    except URLError:
        if not quiet: 
            print 'Error - could not connect to Google.com'
            print 'Checking internet connectivity.'
            if connected():
                print 'You appear to be connected to the internet.'
            else:
                print 'You appear to be disconnected from the internet.'
            #bug_report()
        exit(1)

def parse(data, query, quiet=False):
    '''Return a dictionary containing definitions and their categories parsed
    from data in JSON.'''
    try:
        dicts = literal_eval(data)['primaries']
        categories = []
        definitions = []
        category = '    ―'
        syllables = ''
        phonetic = ''
        for i, _ in enumerate(dicts):
            if dicts[i]['terms'][0].has_key('labels'):
                category = dicts[i]['terms'][0]['labels'][0]['text']
            categories.append(category)
            syllables = dicts[i]['terms'][0]['text']
            if dicts[i]['terms'][1]['type'] == 'phonetic':
                phonetic = dicts[i]['terms'][1]['text']
            definition = dicts[i]['entries']
            temp_defs = []
            for i, _ in enumerate(definition):
                if definition[i]['type'] == 'meaning':
                    temp_defs.append(definition[i]['terms'][0]['text'])
            definitions.append(temp_defs)
        names = syllables, phonetic
    except KeyError:
        if not quiet:
            print 'No definition found for "%s".' % query
            #bug_report()    
        exit(1)
    return zip(categories, definitions), names

def format_indentation(string, width, indentation=4, bullet='•'):
    '''Parse and print input indented.'''
    indentation *= ' '
    bullet = '  ' + bullet + ' '
    lines = list()
    line_length = width - len(indentation)
    num_lines = int(ceil(len(string) / line_length))
    words = string.split()
    line = words[0]
    index = 0 
    for i in xrange(num_lines):
        for j, word in enumerate(words[(index + 1):], index + 1):
            temp_line = line
            line += ' ' + word
            if len(line) > line_length:
                line = temp_line
                index = j
                break
        lines.append(indentation + line)
        line = words[index]
    lines[0] = bullet + lines[0][4:]
    return lines

def format_output(input, limit, indentation=4, bullet='•'):
    '''Parse and print input list in a specific manner. Only return limit
    number of definitions.'''
    data = input[0]
    names = input[1]
    cols = int(popen('stty size', 'r').read().split()[1])
    if len([item for item in names if item != '']) == 2: 
        print indentation * ' ' + '  ―  '.join(names)
    else:
        print indentation * ' ' + ''.join([only for only in names])
    # TODO Add examples.
    for category in data:
        if category[0] != '':
            print category[0]
        for definition in category[1][:limit]:
            for line in format_indentation(untag(definition), cols,
                                           indentation, bullet):
                print line

def untag(string):
    '''Remove XML tags from string.'''
    return sub('<[^<]+?>', '', string).strip()

def connected():
    '''Return True if connected to the internet, otherwise return False.'''
    try:
        urlopen('http://74.125.113.99', timeout=1)
        return True
    except URLError:
        return False

def bug_report():
    '''Ask user and open a new issue on github.'''
    response = raw_input('This may be a bug. Report issue (yes/no)?\n')
    if response in ['Y', 'YES', 'Yes', 'y', 'yes']:
        open_browser('https://github.com/haukurpallh/def/issues/new')

if __name__ == '__main__':
    parser = ArgumentParser()
    # TODO Fix indentation problems withouth metavar='' and add a long option.
    parser.add_argument('-sl', metavar='', action='append',
                        help='specify a source language, only "en" supported')
    parser.add_argument('-tl', metavar='', action='append',
                        help='specify a target language, only "en" supported')
    parser.add_argument('-n', metavar='', type=int, help='specify the number '
                        + 'of definitions to print for each word category')
    parser.add_argument('-b', metavar='', choices='ndtw', help='specify a '
                        + 'type of bullet; n: normal, d: dash, t: triangular '
                        + 'and w: white')
    # TODO Add an option to print the definitions for each word in a file.
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not print error messages')
    parser.add_argument('query', help='look up the meaning of the word or '
                        + 'concept; requires quotes if longer than one word')
    args = parser.parse_args()
    # TODO Only English seems to work at the moment - check later. Remove
    # language options if not relevant.
    langs = ['en', 'en']
    if args.sl != None:
        langs[0] = args.sl[0]
    if args.tl != None:
        langs[1] = args.tl[0]
    if args.n == None:
        # Show us 3 definitions of each category by default.
        args.n = 3
    if args.b == None or args.b == 'n':
        # Use normal bullets if specified and by default
        args.b = '•'
    elif args.b == 'd':
        args.b = '―'
    elif args.b == 't':
        args.b = '‣'
    elif args.b == 'w':
        args.b = '◦'
    try:
        data = parse(get_data(args.query, langs[0], langs[1], args.quiet),
                     args.query, args.quiet)
        format_output([data[0], data[1]], args.n, bullet=args.b)
    except KeyboardInterrupt:
        print
        exit(130)
