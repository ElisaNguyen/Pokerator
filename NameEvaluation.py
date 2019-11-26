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
    return unique_ngrams, count_ngram


def probability(bigram, unigram, V):
    k = 1
    prob = (bigram + k) / (unigram + (k * V))
    return prob

def probability_list(vocab, bi_count, uni_count, V):
    propability_list_bigram = {}

    for bigram in vocab:
        first, second = bigram
        prob_bigram = probability(bi_count[bigram], uni_count[first], V)
        propability_list_bigram[bigram] = prob_bigram
    return propability_list_bigram

# def evaluation():
#     input = "Pokemon"
#     input_unigram = list(input.lower())
#     input_bigrams = list(ngrams(input_unigram, 2))
#
#     for bigram in input_bigrams:
#         prob = probability(bigram, )

def run():
    bigram_list, unigram_list, V = ngram_lists()
    bigram_vocab, bigram_count = frequency_count(bigram_list)
    unigram_vocab, unigram_count = frequency_count(unigram_list)

    bigram_probabilities = probability_list(bigram_vocab, bigram_count, unigram_count, V)




