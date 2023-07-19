#!/usr/bin/env python3

import ply.lex as lex
import pds3tokens
import sys


def build_lexer():
    return lex.lex(module=pds3tokens)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    lexer = build_lexer()
    with open(argv[1]) as f:
        data = f.read()
        lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == '__main__':
    sys.exit(main())
