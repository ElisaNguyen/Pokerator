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


def load_poke_data():
    poke_data = pd.read_csv("Data/pokemon.csv")
    poke_df = pd.DataFrame(poke_data)
    return poke_df


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


def merge_data_sets():
    poke_df = load_poke_data()
    cmu_entries = load_cmu_data()
    data = []
    data.extend(cmu_entries)
    # data.extend(np.random.choice(cmu_entries, 20000))
    for name in poke_df["name"]:
        if name in re.findall("[a-zA-Z]*", name):
            data.append(name)
        else:
            pass
    return data


# creates a bigram and a unigram list from the data set
def ngram_lists_syllables():
    """
    Creates unigrams and bigrams from the training corpus based on the syllables of words

    :return bigram_list: list of all the syllable bigrams that were created
    :return unigram_list: list of all the syllable unigrams that were created
    :return V: size of the vocabulary of the bigrams
    """
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


def ngram_lists_characters():
    """
    Creates unigrams and bigrams from the training corpus based on the characters of words

    :return bigram_list: list of all the character bigrams that were created
    :return unigram_list: list of all the character unigrams that were created
    :return V: size of the bigram vocabulary of the training data
    """
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
    """
    Creates a list of unique ngrams and counts the frequency of the ngrams of the input list

    :param ngram_list: a list of all the ngrams in the training data
    :return unique_ngrams: list which contains each ngram once
    :return count_gram: dictionary with the ngram as the key and its count in the training set as the value
    """
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


def probability(bi_count, uni_count, V):
    """
    Calculates the Naive Bayes probability of a bigram with k-smoothing

    :param bi_count: count of the occurrence of the bigram in the training set
    :param uni_count: count of the occurrence of the first unigram of the bigram in the training data
    :param V: size of the bigram vocabulary of the training data
    :return: the posterior probability of a bigram
    """
    k = 1
    prob = math.log2((bi_count + k) / (uni_count + (k * V)))
    return prob


def create_model(vocab, bi_count, uni_count, V, path):
    """
    Calculates and stores a model with a bigram as the dictionary key and its probability as the value

    :param vocab: unique list of bigrams of training set
    :param bi_count: count of bigram in the training set
    :param uni_count: count of unigram in the training set
    :param V: size of the bigram vocabulary of the training set
    :param path: path under which to store the model
    :return: dictionary with bigram as key and its probability as the value
    """
    propability_list_bigram = {}

    for bigram in vocab:
        first, second = bigram
        prob_bigram = probability(bi_count[bigram], uni_count[first], V)
        propability_list_bigram[bigram] = prob_bigram

    pickle.dump(propability_list_bigram, open(path, "wb"))
    return propability_list_bigram


def evaluation_prob(input_bigrams, input_unigram, prob_list, uni_count, V):
    """
    Calculates the probability of the input word

    :param input_bigrams: a list of the bigrams of the input word
    :param input_unigram: a list of the unigrams of the input word
    :param prob_list: model with the stored probabilites for each bigram of the training set
    :param uni_count: count of occurrence of a unigram in the training set
    :param V: size of the bigram vocabulary of the training set
    :return: probability of the input word
    """
    prob = 0
    for bigram in input_bigrams:
        first, second = bigram
        if bigram in prob_list:
            prob += prob_list[bigram]
        else:
            if first in uni_count:
                prob += math.log2((0 + 1) / (uni_count[first] + (1 * V)))
            else:
                prob += math.log2((0 + 1) / (0 + (1 * V)))
    prob = (prob / len(input_unigram))
    prob = 2**prob
    return prob


def evaluation_syllable(poke_name, uni_count, V):
    """
    Evaluates an input word that has several syllables based on its syllables

    :param poke_name: input word
    :param uni_count: count of occurrence of a unigram in the training set
    :param V: size of the bigram vocabulary of the training set
    :return: probability of the input word
    """
    prob = 0
    input_name = poke_name
    tok = sequencing.SyllableTokenizer()
    input_unigram = tok.tokenize(input_name.lower())
    input_bigrams = list(ngrams(input_unigram, 2))
    prob_list = pickle.load(open("Data/model_syllables.pckl", "rb"))
    prob = evaluation_prob(input_bigrams, input_unigram, prob_list, uni_count, V)
    return prob


def evaluation_character(poke_name, uni_count, V):
    """
    Evaluates an input word with an artifical suffix based on its characters

    :param poke_name: input word
    :param uni_count: count of occurrence of a unigram in the training set
    :param V: size of the bigram vocabulary of the training set
    :return: probability of the input word
    """
    prob = 0
    input_name = poke_name
    endings = ['saur', 'bat', 'puff', 'duck', 'don', 'gon', 'bull', 'low', 'pede', 'no', 'ta']
    for suffix in endings:
        if input_name.endswith(suffix):
            input_name = input_name.replace(suffix, '')
            input_unigram = list(input_name.lower())
            input_bigrams = list(ngrams(input_unigram, 2))
            char_prob_list = pickle.load(open("Data/model_characters.pckl", "rb"))
            prob = evaluation_prob(input_bigrams, input_unigram, char_prob_list, uni_count, V)
            input_name = poke_name
            break
    return prob

def run():
    """
    Evaluates a list of input names and decides which one is the best name

    :return: best input name
    """
    bigram_list_syl, unigram_list_syl, V_syl = ngram_lists_syllables()
    # bigram_vocab_syl, bigram_count_syl = frequency_count(bigram_list_syl)
    unigram_vocab_syl, unigram_count_syl = frequency_count(unigram_list_syl)

    bigram_list_char, unigram_list_char, V_char = ngram_lists_characters()
    # bigram_vocab_char, bigram_count_char = frequency_count(bigram_list_char)
    unigram_vocab_char, unigram_count_char = frequency_count(unigram_list_char)

    # syllable_probabilities = create_model(bigram_vocab_syl, bigram_count_syl, unigram_count_syl, V_syl, "Data/model_syllables.pckl")
    # character_probabilities = create_model(bigram_vocab_char, bigram_count_char, unigram_count_char, V_char, "Data/model_characters.pckl")

    endings = ['saur', 'bat', 'puff', 'duck', 'don', 'gon', 'bull', 'low', 'pede', 'no', 'ta']
    input_name = ['Girlpede', 'Pengnolia', 'Penguingnolia', 'Penlia', 'Penguinlia', 'MaPenguin', 'MagnoPenguin', 'Maguin', 'Magnoguin']
    input_probs = {}

    for name in input_name:
        for suffix in endings:
            if not name.endswith(suffix):
                prob = evaluation_syllable(name, unigram_count_syl, V_syl)
                input_probs[name] = prob
                print(name, prob)
            else:
                prob = evaluation_character(name, unigram_count_char, V_char)
                input_probs[name] = prob
                print(name, prob)
                break

    best_name = max(input_probs)
    print(best_name)

    return best_name




