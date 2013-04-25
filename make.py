#!/usr/bin/env python
from os.path import join, dirname
import logging
import sys
import os

import bootrst

PAGES = join(dirname(__file__), 'pages')
OUTPUT = join(dirname(__file__), 'www')

def get_files(folder):
    '''Get '*.rst' files in the given `folder`'''
    return [join(folder, fname) for fname in os.listdir(folder)
                                             if fname.startswith('.rst')]

def split_sep(lines):
    '''Split lines by the separator: '\n::\n\n' or a double colon with blank
    lines on either side.'''

    for i in xrange(2, len(lines)):
        if (not lines[i-2].strip() and
            lines[i-1].strip() == '::' and
            not lines[i].strip()):
            return lines[:i-2], ''.join(lines[i+1:])
    return False

def parse_head(headlines):
    '''Parse the head into a dictionary'''
    return {k.strip().lower():v.strip() for k,v in
            (line.split(':', 1) for line in headlines
                if line.strip() and ':' in line)}

def parse_file(fname):
    '''Process a file'''
    text = open(fname).readlines()
    parts = split_sep(text)
    if not parts:
        logging.warn('Head not found in {}'.format(fname))
        return False
    head, body = parts
    options = parse_head(head)
    if not 'title' in head:
        logging.warn('No title given for {}'.format(fname))
        head['title'] = 'Untitled'
    body = bootrst.publish(body)
    return head, body

def verify_dir(dirname):
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
        except:
            logging.error('Unable to create output directory')
            sys.exit(2)

def main():
    verify_dir(OUTPUT)
    files = get_files(PAGES)
    if not files:
        logging.error('No files found')
        sys.exit(1)
    # parse all the files
    parsed = {}
    nav = []
    for fname in files:
        head, body = parse_file(fname)
        nav.append([name, head['title']])


# vim: et sw=4 sts=4
