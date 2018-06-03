import argparse
# import functools
# import re
import sys

import markovify

# import argparse

# import MeCab

# mecab = MeCab.Tagger()

# splitted_text = ""

# # these chars might break markovify
# # https://github.com/jsvine/markovify/issues/84
# BREAKING_CHARS = [
#     '(',
#     ')',
#     '[',
#     ']',
#     '"',
#     "'",
# ]

# with open('toots.cleaned.txt') as fp:
#     splitted_text = ''

#     # split whole text to sentences by newline, and split sentence to words by space.
#     for line in fp:
#         mp = mecab.parseToNode(line)
#         while mp:
#             try:
#                 if mp.surface not in breaking_chars:
#                     splitted_text += mp.surface  # skip if node is markovify breaking char
#                 if mp.surface != '。' and mp.surface != '、':
#                     splitted_text += ' '  # split words by space
#                 if mp.surface == '。':
#                     splitted_text += '\n'  # reresent sentence by newline
#             except UnicodeDecodeError as e:
#                 # sometimes error occurs
#                 print(line)
#             finally:
#                 mp = mp.next

# text_model = markovify.NewlineText(splitted_text, state_size=2)

# with open('markov.data', 'w+') as dp:
#     dp.write(text_model.to_json())

# def mecab_parse(fileobj):
#     mecab = MeCab.Tagger()

#     for line in fileobj:
#         mp = mecab.parseToNode(line)
#         while mp:
#             yield mp
#             mp = mp.next

# def parse(fileobj):
#     for mp in mecab_parse(fileobj):
#         try:
#             if mp.surface not in BREAKING_CHARS:
#                 yield mp.surface
#             if mp.surface != '。' and mp.surface != '、':
#                 yield ' '
#             if mp.surface == '。':
#                 yield '\n'


def learn(infile, outfile):
    model = markovify.NewlineText(infile.read(), state_size=2)
    outfile.write(model.to_json())


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    opts = parser.parse_args(argv)
    learn(opts.target, opts.output)


if __name__ == '__main__':
    rc = main()
    if rc is None:
        sys.exit(0)
    elif isinstance(rc, int):
        sys.exit(rc)
    else:
        print(rc)
        sys.exit(-1)
