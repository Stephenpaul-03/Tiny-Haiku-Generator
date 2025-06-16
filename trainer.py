import os
import re
import pickle
import markovify
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import cmudict

nltk.download('punkt')

BOOKS_FOLDER = "Books"
MODEL_FOLDER = "Trained_Models"
os.makedirs(MODEL_FOLDER, exist_ok=True)

cmu_dict = cmudict.dict()

VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
EXCEPTIONS = re.compile("[^aeiou]e[sd]?$|[^e]ely$", flags=re.I)
ADDITIONAL = re.compile("[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|.y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua", flags=re.I)

def count_syllables(word):
    try:
        return [len([y for y in x if y[-1].isdigit()]) for x in cmu_dict[word.lower()]][0]
    except KeyError:
        return weak_count_syllables(word)

def weak_count_syllables(word):
    vowel_runs = len(VOWEL_RUNS.findall(word))
    exceptions = len(EXCEPTIONS.findall(word))
    additional = len(ADDITIONAL.findall(word))
    return max(1, vowel_runs - exceptions + additional)

def syllables_counter(line):
    return sum(count_syllables(word) for word in line.split())

def cleaner(text):
    start = re.search(r"\*{3} START OF.*?\*{3}", text)
    end = re.search(r"\*{3} END OF.*?\*{3}", text)
    if start and end:
        return text[start.end():end.start()]
    return text

def trainer(book_path, model_path):
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    from scraper import reader  # lazy import to avoid circular dependencies
    raw_text = reader(book_path)
    cleaned_text = cleaner(raw_text)

    if len(cleaned_text.split()) < 100:
        print("Cleaned text too short. Using raw text.")
        cleaned_text = raw_text

    tokenizer = PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(cleaned_text)
    text_model = markovify.Text("\n".join(sentences), state_size=1)

    with open(model_path, 'wb') as f:
        pickle.dump(text_model, f)

    return text_model

def generator(model):
    structure = [5, 7, 5]
    haiku = []

    for target in structure:
        for _ in range(100):
            sentence = model.make_short_sentence(100, tries=100)
            if sentence and syllables_counter(sentence) == target:
                haiku.append(sentence)
                break
        else:
            haiku.append("(line unavailable)")

    return "\n".join(haiku)
