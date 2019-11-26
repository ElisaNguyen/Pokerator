"""Choose best
Likelihood of letters appearing in that order (n-grams of CMU dict or pokedex?)
→ Namelette in “Checking the phonetic likelihood of the new word”
In case all are bad: pokemon suffixes? (e.g. horsemon)"""

import pandas as pd
from nltk.util import ngrams


def load_data():
    # load the pokemon data with all the names
    poke_data = pd.read_csv("Data/pokemon.csv")
    poke_df = pd.DataFrame(poke_data)
    return poke_df

def ngram_lists():
    # create a n-gram list with the n-grams from all the pokemon names
    df = load_data()
    poke_bigram_list = []
    poke_unigram_list = []
    for name in df['name']:
        characters = list(name.lower())
        n_grams = list(ngrams(characters, 2))
        poke_bigram_list.extend(n_grams)
        poke_unigram_list.extend(characters)

    V = len(poke_unigram_list)
    return poke_bigram_list, poke_unigram_list, V

# counts the frequency of the n-gram in question, input the n-gram list
def frequency_count(poke_ngram_list):
    unique_ngrams = []
    for ngram in poke_ngram_list:
        if ngram in unique_ngrams:
            pass
        else:
            unique_ngrams.append(ngram)
    count_ngram = {}
    for ngram in unique_ngrams:
        count_ngram[ngram] = poke_ngram_list.count(ngram)
    return count_ngram


def probability(bigram, unigram, V):
    k = 1
    prob = (bigram + k) / (unigram + (k * V))
    return prob

def run():
    bigram_list, unigram_list, V = ngram_lists()
    bigram_count = frequency_count(bigram_list)
    unigram_count = frequency_count(unigram_list)

    input = "Pokemon"
    input_unigram = list(input.lower())
    input_n_grams = list(ngrams(input_unigram, 2))

