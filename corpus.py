import argparse
import sys

import MeCab

# these chars might break markovify
# https://github.com/jsvine/markovify/issues/84
BREAKING_CHARS = [
    '(',
    ')',
    '[',
    ']',
    '"',
    "'",
]

tagger = MeCab.Tagger('-Ochasen')


def mecab_parse(fileobj):
    for line in fileobj:
        try:
            node = tagger.parseToNode(line.strip())
            sys.stdout.write('.')
            sys.stdout.flush()
            while node:
                yield node.surface
                node = node.next
        except Exception:
            pass
    sys.stdout.write('\n')
    sys.stdout.flush()


def corpus(fileobj):
    before = ''
    for sentence in mecab_parse(fileobj):
        try:
            if sentence == before:
                continue
            before = sentence

            if sentence not in BREAKING_CHARS:
                yield sentence.strip()
            if sentence != '。' and sentence != '、':
                yield ' '
            if sentence == '。':
                yield '\n'
        except Exception:
            pass


def run_corpus(infile, outfile):
    for sentence in corpus(infile):
        outfile.write(sentence)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    opts = parser.parse_args(argv)
    run_corpus(opts.target, opts.output)


if __name__ == '__main__':
    rc = main()
    if rc is None:
        sys.exit(0)
    elif isinstance(rc, int):
        sys.exit(rc)
    else:
        print(rc)
        sys.exit(-1)
