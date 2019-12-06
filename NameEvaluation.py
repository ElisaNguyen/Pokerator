"""Choose best
Likelihood of letters appearing in that order (n-grams of CMU dict or pokedex?)
→ Namelette in “Checking the phonetic likelihood of the new word”
In case all are bad: pokemon suffixes? (e.g. horsemon)"""

import pickle
import nltk
import pandas as pd
import nltk.tokenize.sonority_sequencing as sequencing
from nltk.util import ngrams
import math
import re
import numpy as np
nltk.download('cmudict')


# loads the pokemon dataset
def load_poke_data():
    # load the pokemon data with all the names
    poke_data = pd.read_csv("Data/pokemon.csv")
    poke_df = pd.DataFrame(poke_data)
    return poke_df


# loads the cmu dictionary
def load_cmu_data():
    entries = nltk.corpus.cmudict.entries()
    cmu_data = []
    for item in entries:
        word, pronunciation = item
        if word in re.findall("[a-zA-Z]{2,}", word):
            cmu_data.append(word)
        else:
            pass
    return cmu_data


# merges the pokemon dataset and the cmu dictionary into one dataset
def merge_data_sets():
    poke_df = load_poke_data()
    cmu_entries = load_cmu_data()
    # print(poke_df["name"])
    data = []
    data.extend(np.random.choice(cmu_entries, 2000))
    for name in poke_df["name"]:
        if name in re.findall("[a-zA-Z]*", name):
            data.append(name)
        else:
            pass
    # print(data[113500:])
    return data


# creates a bigram and a unigram list from the data set
def ngram_lists_syllables():
    data = merge_data_sets()
    bigram_list = []
    unigram_list = []
    tok = sequencing.SyllableTokenizer()
    for word in data:
        if len(tok.tokenize(word)) >= 2:
            syllables = tok.tokenize(word.lower())
            bigrams = list(ngrams(syllables, 2))
            bigram_list.extend(bigrams)
            unigram_list.extend(syllables)
        else:
            pass
    V = len(bigram_list)
    return bigram_list, unigram_list, V

#TODO filter Wörter mit einem Character raus, um dann ein Model zu trainieren das auch einsilbige Wörter enthält
def ngram_lists_characters():
    data = merge_data_sets()
    bigram_list = []
    unigram_list = []
    for word in data:
        characters = list(word.lower())
        bigrams = list(ngrams(characters, 2))
        bigram_list.extend(bigrams)
        unigram_list.extend(characters)
    V = len(bigram_list)
    return bigram_list, unigram_list, V

# counts the frequency of the n-gram in question, input the n-gram list
def frequency_count(ngram_list):
    unique_ngrams = []
    for ngram in ngram_list:
        if ngram in unique_ngrams:
            pass
        else:
            unique_ngrams.append(ngram)
    count_ngram = {}
    for ngram in unique_ngrams:
        count_ngram[ngram] = ngram_list.count(ngram)
    return unique_ngrams, count_ngram


def probability(bigram, unigram, V):
    k = 1
    prob = math.log2((bigram + k) / (unigram + (k * V)))
    return prob


# takes the unigram and bigram counts as input and calculates the probability for each bigram and stores this in a dictionary
def probability_list(vocab, bi_count, uni_count, V, path):
    propability_list_bigram = {}

    for bigram in vocab:
        first, second = bigram
        prob_bigram = probability(bi_count[bigram], uni_count[first], V)
        propability_list_bigram[bigram] = prob_bigram

    pickle.dump(propability_list_bigram, open(path, "wb"))
    return propability_list_bigram

#TODO wenn wort nur eine silbe, dann suffix wegschmeißen und das einsilbige Wort auf Characterbasis evaluieren
def evaluation(poke_name, uni_count, V):
    input = poke_name
    tok = sequencing.SyllableTokenizer()
    endings = ['saur', 'bat', 'puff', 'duck', 'don', 'gon', 'bull', 'low', 'pede', 'no', 'ta']


    if input.endswith(endings):
        for suffix in endings:
            input.strip(suffix)
        input_char = list(input.lower())
        input_char_bigrams = list(ngrams(input_char, 2))
    else:
        input_unigram = tok.tokenize(input.lower())
        input_bigrams = list(ngrams(input_unigram, 2))
        prob_list = pickle.load(open("Data/model.pckl", "rb"))

    prob = 0
    for bigram in input_bigrams:
        first, second = bigram
        print(bigram)
        if bigram in prob_list:
            prob += prob_list[bigram]
            print(prob)
        else:
            if first in uni_count:
                prob += math.log2((0 + 1) / (uni_count[first] + (1 * V)))
                print(uni_count[first])
            else:
                prob += math.log2((0 + 1) / (0 + (1 * V)))
                print("unigram not in traindata")
    prob = (prob / len(input_unigram))
    prob = 2**prob
    return prob


def run():
    bigram_list, unigram_list, V = ngram_lists_syllables()
    bigram_vocab, bigram_count = frequency_count(bigram_list)
    unigram_vocab, unigram_count = frequency_count(unigram_list)

    # bigram_probabilities = probability_list(bigram_vocab, bigram_count, unigram_count, V, "Data/model.pckl")
    likelihood = evaluation("dtimon", unigram_count, V)
    print(likelihood)
    return likelihood




