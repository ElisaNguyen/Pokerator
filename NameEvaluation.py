"""Choose best
Likelihood of letters appearing in that order (n-grams of CMU dict or pokedex?)
→ Namelette in “Checking the phonetic likelihood of the new word”
In case all are bad: pokemon suffixes? (e.g. horsemon)"""
import numpy as np
import pickle
import nltk
import pandas as pd
import nltk.tokenize.sonority_sequencing as sequencing
from nltk.util import ngrams
import math
import re
import operator
nltk.download('cmudict')


def load_poke_data():
    poke_data = pd.read_csv("Data/pokemon.csv")
    poke_df = pd.DataFrame(poke_data)
    poke_data = []
    for name in poke_df["name"]:
        if name in re.findall("[a-zA-Z]*", name):
            poke_data.append(name)
        else:
            pass
    return poke_data


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
def ngram_lists_syllables(data):
    """
    Creates unigrams and bigrams from the training corpus based on the syllables of words

    :return bigram_list: list of all the syllable bigrams that were created
    :return unigram_list: list of all the syllable unigrams that were created
    :return V: size of the vocabulary of the bigrams
    """
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


def ngram_lists_characters(data):
    """
    Creates unigrams and bigrams from the training corpus based on the characters of words

    :return bigram_list: list of all the character bigrams that were created
    :return unigram_list: list of all the character unigrams that were created
    :return V: size of the bigram vocabulary of the training data
    """
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

    pickle.dump([propability_list_bigram, uni_count, V], open(path, "wb"))
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
            prob += 2**prob_list[bigram]
        else:
            if first in uni_count:
                prob += ((0 + 1) / (uni_count[first] + (1 * V)))
            else:
                prob += ((0 + 1) / (0 + (1 * V)))
    prob = (prob / len(input_unigram))
    # prob = 2**prob

    return prob


def evaluation_syllable(poke_name):
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
    prob_list_poke, uni_count_poke, V_poke = pickle.load(
        open("Data/model_syllables_poke.pckl", "rb"))
    prob_list_cmu, uni_count_cmu, V_cmu = pickle.load(
        open("Data/model_syllables_cmu.pckl", "rb"))

    input_unigram = tok.tokenize(input_name.lower())
    input_bigrams = list(ngrams(input_unigram, 2))
    for i in np.arange(0.0, 1.0, 0.1):
        # print("poke", i, "cmu", (1.0 - i))
        prob = (i * evaluation_prob(input_bigrams, input_unigram, prob_list_poke, uni_count_poke, V_poke)) \
               + ((1.0-i) * evaluation_prob(input_bigrams, input_unigram, prob_list_cmu, uni_count_cmu, V_cmu))
    return prob, i


def evaluation_character(poke_name):
    """
    Evaluates an input word with an artificial suffix based on its characters

    :param poke_name: input word
    :param uni_count: count of occurrence of a unigram in the training set
    :param V: size of the bigram vocabulary of the training set
    :return: probability of the input word
    """
    prob = 0
    input_name = poke_name
    prob_list_poke, uni_count_poke, V_poke = pickle.load(open("Data/model_characters_poke.pckl", "rb"))
    prob_list_cmu, uni_count_cmu, V_cmu = pickle.load(open("Data/model_characters_cmu.pckl", "rb"))
    endings = ['saur', 'bat', 'puff', 'duck', 'don', 'gon', 'bull', 'low', 'pede', 'no', 'ta']

    for suffix in endings:
        if input_name.endswith(suffix):
            input_name = input_name.replace(suffix, '')
            input_unigram = list(input_name.lower())
            input_bigrams = list(ngrams(input_unigram, 2))
            for i in np.arange(0.0, 1.0, 0.1):
                # print("poke", i, "cmu", (1.0-i))
                prob = (i * evaluation_prob(input_bigrams, input_unigram, prob_list_poke, uni_count_poke, V_poke))\
                    + ((1.0-i) * evaluation_prob(input_bigrams, input_unigram, prob_list_cmu, uni_count_cmu, V_cmu))
            input_name = poke_name
            break
    return prob, i

def evaluation_name(blended_words):
    """
    Evaluates a list of input names and decides which one is the best name

    :return: best input name
    """
    # poke_data = load_poke_data()
    # bigram_list_syl_poke, unigram_list_syl_poke, V_syl_poke = ngram_lists_syllables(poke_data)
    # bigram_vocab_syl_poke, bigram_count_syl_poke = frequency_count(bigram_list_syl_poke)
    # unigram_vocab_syl_poke, unigram_count_syl_poke = frequency_count(unigram_list_syl_poke)
    #
    # bigram_list_char_poke, unigram_list_char_poke, V_char_poke = ngram_lists_characters(poke_data)
    # bigram_vocab_char_poke, bigram_count_char_poke = frequency_count(bigram_list_char_poke)
    # unigram_vocab_char_poke, unigram_count_char_poke = frequency_count(unigram_list_char_poke)
    #
    # syllable_probabilities_poke = create_model(bigram_vocab_syl_poke, bigram_count_syl_poke, unigram_count_syl_poke,
    #                                       V_syl_poke, "Data/model_syllables_poke.pckl")
    # character_probabilities_poke = create_model(bigram_vocab_char_poke, bigram_count_char_poke, unigram_count_char_poke,
    #                                        V_char_poke, "Data/model_characters_poke.pckl")
    #
    cmu_data = load_cmu_data()
    # bigram_list_syl_cmu, unigram_list_syl_cmu, V_syl_cmu = ngram_lists_syllables(cmu_data)
    # bigram_vocab_syl_cmu, bigram_count_syl_cmu = frequency_count(bigram_list_syl_cmu)
    # unigram_vocab_syl_cmu, unigram_count_syl_cmu = frequency_count(unigram_list_syl_cmu)
    #
    # bigram_list_char_cmu, unigram_list_char_cmu, V_char_cmu = ngram_lists_characters(cmu_data)
    # bigram_vocab_char_cmu, bigram_count_char_cmu = frequency_count(bigram_list_char_cmu)
    # unigram_vocab_char_cmu, unigram_count_char_cmu = frequency_count(unigram_list_char_cmu)
    #
    # syllable_probabilities_cmu = create_model(bigram_vocab_syl_cmu, bigram_count_syl_cmu, unigram_count_syl_cmu,
    #                                       V_syl_cmu, "Data/model_syllables_cmu.pckl")
    # character_probabilities_cmu = create_model(bigram_vocab_char_cmu, bigram_count_char_cmu, unigram_count_char_cmu,
    #                                        V_char_cmu, "Data/model_characters_cmu.pckl")

    endings = ['saur', 'bat', 'puff', 'duck', 'don', 'gon', 'bull', 'low', 'pede', 'no', 'ta']
    input_probs = {}

    for name in blended_words:
        if name in cmu_data:
            pass
        else:
            for suffix in endings:
                if name.endswith(suffix):
                    prob, i = evaluation_character(name)
                    input_probs[name, i] = prob
                    break
                else:
                    prob, i = evaluation_syllable(name)
                    input_probs[name, i] = prob

    print(input_probs)
    best_name = max(input_probs.items(), key=operator.itemgetter(1))[0]
    print(best_name)

    return best_name




