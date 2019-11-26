#Find synonyms to answers using WordNet
#Blend words together
import nltk.tokenize.sonority_sequencing as sequencing
import requests
import pandas as pd
import re


def blend_words(word_dict):
    df = pd.DataFrame(columns=['word', 'question', 'synonyms'])
    df['word'] = word_dict.values()
    df['question'] = word_dict.keys()
    df['synonyms'] = df['word'].apply(synonyms)
    return df


def blend_a_word(word1, word2):
    tok = sequencing.SyllableTokenizer()
    sil1 = tok.tokenize(word1)
    sil2 = tok.tokenize(word2)
    longer_word = sil1 if len(sil1) > len(sil2) else sil2
    shorter_word = sil2 if len(sil1) > len(sil2) else sil1


def synonyms(word):
    texts, synonyms = conceptnet_request(word, 'RelatedTo')
    return synonyms


def conceptnet_request(word, relation):
    url = 'http://api.conceptnet.io/c/en/' + word + '?rel=/r/' + relation + '&limit=10'
    print(url)
    response = requests.get(url).json()
    df = pd.DataFrame(response['edges'])
    surface_texts = list(df[df['rel'].apply(lambda e: dict(e)['label'] == relation)]['surfaceText'])
    words = [e.replace('[', '').replace(']', '') for e in re.findall("\[+[a-z A-Z]+\]+", str(surface_texts))]
    words = list(set(words))
    words.remove(word)
    return surface_texts, words

