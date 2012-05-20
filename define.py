#!/usr/bin/python
#encoding: utf8

from ast import literal_eval
from os import popen
from re import sub
from string import capitalize
from sys import argv, exit
from urllib import urlencode
from urllib2 import urlopen, URLError

def get_data(word, src_lan='en', tgt_lan='en', silent=False):
    '''Return data in JSON from Google.''' 
    base_url = 'http://www.google.com/dictionary/json?callback=c&'
    options = urlencode({'q': word, 'sl': src_lan, 'tl': tgt_lan})
    try:
        return urlopen(base_url + options).read().decode('utf8')
    except URLError:
        if not silent: 
            print 'Error - could not connect to Google.com'
            print 'Checking internet connectivity.'
            if connected():
                print 'You appear to be connected to the internet. Try again.'
            else:
                print 'You appear to be disconnected from the internet.'
        exit()

def parse(data, silent=False):
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
        if not silent:
            print 'No definitions found for "%s".' % ' '.join(argv[1:])
        exit()
    return zip(categories, definitions)

def format_output(input, limit=3):
    '''Parse and print input list in a specific manner.'''
    #cols = int(popen('stty size', 'r').read().split()[1])
    print '    %s' % capitalize(' '.join(input[0]))
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
    if len(argv) != 1:
        try:
            format_output([argv[1:], parse(get_data(' '.join(argv[1:])))])
        except KeyboardInterrupt:
            print
            exit()
