import argparse
import sys

import markovify

NG_WORDS = []
END_WORDS = []


class SentenceGenerationError(Exception):
    pass


def load_model(infile):
    return markovify.Text.from_json(infile.read())


def cleanup_sentence(sentence):
    if sentence:
        sentence = sentence.replace(' ', '').replace('。', '')
        if not any((ng_word in sentence) for ng_word in NG_WORDS):
            for end_word in END_WORDS:
                if end_word in sentence:
                    index = sentence.index(end_word) + len(end_word)
                    first = sentence[:index]
                    second = sentence[index:]
                    return first if len(first) > len(second) else second
            return sentence


def generate_sentence(model, max_chars=50, **kwargs):
    sentence = ''
    for ii in range(3):
        sentence = cleanup_sentence(model.make_short_sentence(max_chars=max_chars, **kwargs))
        if sentence:
            return sentence
    else:
        raise SentenceGenerationError()


def load_ng_words(path):
    global NG_WORDS
    with open(path) as fp:
        NG_WORDS = list(map(lambda line: line.strip(), fp.readlines()))


def load_end_words(path):
    global END_WORDS
    with open(path) as fp:
        END_WORDS = list(map(lambda line: line.strip(), fp.readlines()))


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--ngwords', default='NG_WORDS.txt')
    parser.add_argument('--endwords', default='END_WORDS.txt')
    parser.add_argument('-c', '--count', type=int, default=1)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    opts = parser.parse_args(argv)

    load_ng_words(opts.ngwords)
    load_end_words(opts.endwords)

    model = load_model(opts.target)

    for ii in range(opts.count):
        try:
            sentence = generate_sentence(model)
            if sentence:
                opts.output.write(sentence)
                opts.output.write('\n')
        except SentenceGenerationError:
            pass


if __name__ == '__main__':
    rc = main()
    if rc is None:
        sys.exit(0)
    elif isinstance(rc, int):
        sys.exit(rc)
    else:
        print(rc)
        sys.exit(-1)
