import argparse
import sys

import markovify


class SentenceGenerationError(Exception):
    pass


def load_model(infile):
    return markovify.Text.from_json(infile.read())


def generate_sentence(model, outfile, max_chars=50, **kwargs):
    sentence = model.make_short_sentence(max_chars=max_chars, **kwargs)
    if sentence:
        sentence = sentence.replace(' ', '')
        outfile.write(sentence)
        outfile.write('\n')
    else:
        raise SentenceGenerationError()


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    opts = parser.parse_args(argv)
    model = load_model(opts.target)
    generate_sentence(model, opts.output)


if __name__ == '__main__':
    rc = main()
    if rc is None:
        sys.exit(0)
    elif isinstance(rc, int):
        sys.exit(rc)
    else:
        print(rc)
        sys.exit(-1)
