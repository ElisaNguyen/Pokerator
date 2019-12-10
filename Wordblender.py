#Find synonyms to answers using WordNet
#Blend words together
import os

import nltk.tokenize.sonority_sequencing as sequencing
import pandas as pd
import numpy as np
from ConceptNet import conceptnet_request
import string


def blend_words(word_dict):
    df = pd.DataFrame(columns=['word', 'question', 'synonyms'])
    df['word'] = word_dict.values()
    df['question'] = word_dict.keys()
    df['synonyms'] = df['word'].apply(synonyms)
    return df


def blend_a_word(word1, word2):
    """
    Blends two words together in different variations.

    :param word1: a word
    :param word2: a word
    :return: list of possible blended words
    """
    tok = sequencing.SyllableTokenizer()
    syl1 = tok.tokenize(word1)
    syl2 = tok.tokenize(word2)
    words = []
    if len(syl1) == len(syl2) == 1:
        endings = ['saur', 'bat', 'puff', 'duck', 'don','gon', 'bull', 'low', 'pede','no','ta']
        syl1 = syl1[0]
        syl2 = syl2[0]
        words.append(syl_to_vowel(syl2) + syl_from_vowel(syl1) + np.random.choice(endings))
        words.append(syl_to_vowel(syl1) + syl_from_vowel(syl2) + np.random.choice(endings))
    else:
        longer_word = syl1 if len(syl1) > len(syl2) else syl2
        shorter_word = syl2 if len(syl1) > len(syl2) else syl1
        for i in range(1, len(longer_word)):
            for j in range(1, len(shorter_word)+1):
                words.append(''.join(shorter_word[:j]) + ''.join(longer_word[i:]))
        for i in range(0, len(shorter_word)):
            for j in range(1, len(longer_word)):
                words.append(''.join(longer_word[:j]) + ''.join(shorter_word[i:]))
    return words


def syl_from_vowel(syl):
    """
    Finds the position of the first vowel for a syllable.
    
    :param syl: input syllable
    :return: syllable starting from the first vowel
    """
    vowels = ['a','e','i','u','o','y']
    i = 0
    while syl[i] not in vowels:
        if (len(syl)-1) <= i:
            if i == (len(syl)-1):
                return str(syl[i+1:] + np.random.choice(vowels))
            break
        i += 1
    return str(syl[i:])


def syl_to_vowel(syl):
    """
    Finds the position of the first vowel for a syllable.

    :param syl: input syllable
    :return: syllable ending at the first vowel
    """
    vowels = ['a', 'e', 'i', 'u', 'o', 'y']
    consonants = list(string.ascii_lowercase)
    [consonants.remove(v) for v in vowels]
    i = 0
    while syl[i] not in vowels:
        i += 1
        if (len(syl)) <= i:
            break
    if i == 0:
        return str(np.random.choice(consonants))
    return str(syl[:i])


def synonyms(word):
    """
    Returns a list of synonyms.

    :param word: a word
    :return: list of synonyms
    """
    texts, synonyms = conceptnet_request(word, 'RelatedTo')
    return synonyms





