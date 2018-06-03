import argparse
import os.path
import sys
import time

import requests
from generate_sentence import (
    SentenceGenerationError,
    generate_sentence,
    load_end_words,
    load_model,
    load_ng_words,
)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--ngwords', default='NG_WORDS.txt')
    parser.add_argument('--endwords', default='END_WORDS.txt')
    parser.add_argument('--conf', default='~/.config/mastodon/mstdn.jp.sub/user.txt')
    parser.add_argument('--interval', type=int, default=2)

    opts = parser.parse_args(argv)

    with open(os.path.expanduser(opts.conf)) as fp:
        token = fp.read().strip()

    load_ng_words(opts.ngwords)
    load_end_words(opts.endwords)

    model = load_model(opts.target)

    while not time.sleep(opts.interval):
        try:
            sentence = generate_sentence(model)
            if sentence:
                res = requests.post(
                    'https://mstdn.jp/api/v1/statuses/',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}',
                    },
                    json={
                        'status': sentence,
                        'in_reply_to_id': None,
                        'media_ids': None,
                        'sensitive': None,
                        'spoiler_text': None,
                        'visibility': 'unlisted',
                    })
                print(res)
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
