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
    words = []
    if len(sil1)==len(sil2):
        sil1 = sil1[0]
        sil2 = sil2[0]
        #TODO check for double consonats
        vocals = ['a','e','i','u','o','y']
        i=0
        while sil1[i] not in vocals:
            if (len(sil1)-1)<= i:
                #TODO silbe hat keine Vokale
                break
            i += 1
        #TODO sil2 hat Vokal als ersten Buchstaben
        words.append(sil2[0] + str(sil1[i:]) + 'mon')

        i = 0
        while sil2[i] not in vocals:
            if (len(sil2) - 1) <= i:
                # TODO silbe hat keine Vokale
                break
            i += 1
        words.append(sil1[0] + sil2[i:] + 'mon')
    else:
        longer_word = sil1 if len(sil1) > len(sil2) else sil2
        shorter_word = sil2 if len(sil1) > len(sil2) else sil1
        for i in range(1,len(longer_word)):
            for j in range(1, len(shorter_word)):
                words.append(''.join(shorter_word[:j]) + ''.join(longer_word[i:]))
        for i in range(1, len(shorter_word)):
            for j in range(1, len(longer_word)):
                words.append(''.join(longer_word[:j]) + ''.join(shorter_word[i:]))

    print(words)
    return words


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
    if word in words:
        words.remove(word)
    return surface_texts, words


