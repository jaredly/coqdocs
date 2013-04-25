#!/usr/bin/env python

import sys
import argparse
import subprocess
from subprocess import Popen, PIPE
import pexpect
from xml.sax.saxutils import escape

import pygments
from pygments.lexers import VerilogLexer
from pygments.formatters import HtmlFormatter

def highlight(text):
    return pygments.highlight(text, VerilogLexer(), HtmlFormatter())

def make_parse():
    base = argparse.ArgumentParser('Coq Pretty')
    base.add_argument('input_file')
    base.add_argument('-o', '--outfile', dest='out', default=None)
    return base

class Slave:
    def __init__(self):
        pass

    def write(self):
        pass

    def read(self):
        pass

class PlainSlave:
    nextrx = '\n\w+ < '
    def __init__(self):
        self.slave = pexpect.spawn('coqtop.opt')
        self.slave.expect(self.nextrx)

    def call(self, line):
        self.slave.write(line.replace('\n','') + '\n')
        self.slave.expect(self.nextrx)
        name = self.slave.after[1:].split()[0]
        return name, self.slave.before.split('\r\n', 1)[1] + '\n'

class PexSlave:
    def __init__(self):
        self.slave = pexpect.spawn('coqtop.opt -ideslave')

    def call(self, line):
        cmd = '<call val="interp">{}</call>\n'.format(escape(line.replace('\n','')))
        # write the command
        print 'cmd', [cmd]
        self.slave.write(cmd)
        # get the echo
        echo = self.slave.readline()
        # self.slave.write('\n')
        self.slave.write('\n')
        out = self.slave.readline()
        if not out.strip():
            out = self.slave.readline()
            self.slave.write('\n')
        tag = out[1:out.find('>')].split()[0]
        while '</' + tag + '>' not in out:
            out += self.slave.readline()
        return out

    def write(self, line):
        self.slave.write(line)

class PoSlave:
    def __init__(self):
        self.slave = Popen(['coqtop.opt', '-ideslave'],
                           shell=True, stdin=PIPE, stdout=PIPE)

    def write(self, line):
        self.slave.writeline(line)

    def read(self):
        return self.slave.readline()

def get_fileiter(fname):
    with open(fname) as f:
        at = 0
        buffer = ''
        for line in f:
            buffer += line
            while '.' in buffer:
                at = buffer.find('.')
                yield buffer[:at+1]
                buffer = buffer[at+1:]

def main(args):
    options = make_parse().parse_args(args)
    cmds = get_fileiter(options.input_file)
    coq = PlainSlave()
    if options.out is None:
        out = sys.stdout
    else:
        out = open(options.out, 'w')
    css = HtmlFormatter().get_style_defs('.highlight')
    out.write('<!DOCTYPE html>\n<html>\n<head>\n  <title>Coq Theorem</title>\n')
    out.write('  <style>{}</style><link rel="stylesheet" href="pretty.css">'.format(css))
    out.write('</head>\n<body>\n')
    for line in cmds:
        theorem, result = coq.call(line)
        out.write(('  <div class="step"><div class="cmd">{}</div>\n'
                  '  <div class="response">{}</div></div>\n'
                  '').format(highlight(line), highlight(result)))
        # print 'Sent {0} GOT {2} : now in {1}'.format(line, theorem, [result])
        # print result
    out.write('</body>\n</html>\n')
    out.close()

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: et sw=4 sts=4
