#!/usr/bin/python
#coding: utf8

from argparse import ArgumentParser
from ast import literal_eval
from os import popen
from re import sub
from string import capitalize
from sys import argv, exit
from urllib import urlencode
from urllib2 import urlopen, URLError

def get_data(query, src_lan='en', tgt_lan='en', quiet=False):
    '''Return data in JSON from Google.''' 
    # TODO This IP might not be static - add more IPs in case of errors.
    base_url = 'http://173.194.35.144/dictionary/json?callback=c&'
    options = urlencode({'q': query, 'sl': src_lan, 'tl': tgt_lan})
    try:
        return urlopen(base_url + options).read().decode('utf8')
    except URLError:
        if not quiet: 
            print 'Error - could not connect to Google.com'
            print 'Checking internet connectivity.'
            if connected():
                print 'You appear to be connected to the internet. Try again.'
            else:
                print 'You appear to be disconnected from the internet.'
        exit(1)

def parse(data, query, quiet=False):
    '''Return a dictionary containing definitions and their categories parsed
    from data in JSON.'''
    try:
        dicts = literal_eval(data[2:-10])['primaries']
        categories = []
        definitions = []
        for i, _ in enumerate(dicts):
            category = dicts[i]['terms'][0]['labels'][0]['text']
            categories.append(category)
            definition = dicts[i]['entries']
            temp_defs = []
            for i, _ in enumerate(definition):
                if definition[i].has_key('type'):
                    if definition[i]['type'] == 'meaning':
                        temp_defs.append(definition[i]['terms'][0]['text'])
            definitions.append(temp_defs)
    except KeyError:
        if not quiet:
            print 'No definition found for "%s".' % query
        exit(1)
    return zip(categories, definitions)

def format_output(input, limit):
    '''Parse and print input list in a specific manner. Only return limit
    number of definitions.'''
    # cols = int(popen('stty size', 'r').read().split()[1])
    # NOTE Adjust text if longer than one line (number of columns) so that the
    # output is more readable.
    print '    %s' % capitalize(input[0])
    for category in input[1]:
        print category[0]
        for definition in category[1][:limit]:
            print '  • %s.' % untag(definition)

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

if __name__ == '__main__':
    parser = ArgumentParser()
    # TODO Fix indentation problems withouth metavar='' and add a long option.
    parser.add_argument('-sl', metavar='', action='append',
                        help='specify a source language, e.g. en')
    parser.add_argument('-tl', metavar='', action='append',
                        help='specify a target language, e.g. en')
    parser.add_argument('-n', metavar='', type=int, help='specify the number '
                        + 'of definitions to print for each word category')
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
    try:
        # TODO Make this more readable.
        format_output([args.query, parse(get_data(args.query, langs[0],
                       langs[1], args.quiet), args.query, args.quiet)],
                      args.n)
    except KeyboardInterrupt:
        # Print a newline to start the prompt on an empty line and exit.
        # TODO Do not print "^C".
        print
        exit(130)
