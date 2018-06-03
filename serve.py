import generate_sentence
from flask import Flask

app = Flask(__name__)

generate_sentence.load_ng_words('NG_WORDS.txt')
generate_sentence.load_end_words('END_WORDS.txt')

with open('markov.data') as fp:
    model = generate_sentence.load_model(fp)


@app.route("/")
def index():
    return generate_sentence.generate_sentence(model, retries=100)
