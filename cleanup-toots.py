#! /usr/bin/env python
import argparse
import functools
import re
import sys

PATTERNS = [
    '&gt;',
    '&lt;',
    '<.*?>',  # ex: <p>  </p> <br />
    '@\w+',  # ex: @sximada @sximada123 @sximada_
    '\&quot\;',  # ex: &quot;
    '\-',
    '\r',
    '\u3000',
    '\｜',
    'http[s]://\S+',  # ex: https:example.com/foo/bar/baz
]

REGXS = list(map(re.compile, PATTERNS))

cleanup = functools.partial(
    functools.reduce,
    lambda line, regx: regx.sub('', line),
    REGXS,
)


def clean_toots(infile, outfile):
    line = None
    try:
        for line in infile:
            outfile.write(cleanup(line))
    except Exception:
        raise


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    opts = parser.parse_args(argv)
    clean_toots(opts.target, opts.output)


if __name__ == '__main__':
    rc = main()
    if rc is None:
        sys.exit(0)
    elif isinstance(rc, int):
        sys.exit(rc)
    else:
        print(rc)
        sys.exit(-1)
