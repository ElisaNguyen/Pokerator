import requests
import pandas as pd
import re


def conceptnet_request(word, relation):
    """
    Send an API request to conceptNet for a word and for a certain relation with the word the surface text in which it
    can be used and the related words.

    :param word: a word
    :param relation: a relation of conceptNet
    :return: list of surface texts for the word and the relation and a list of words related to the input word
    """
    url = 'http://api.conceptnet.io/c/en/' + word + '?limit=100'
    print(url)
    response = requests.get(url).json()
    df = pd.DataFrame(response['edges'])
    surface_texts = list(df[df['rel'].apply(lambda e: dict(e)['label'] == relation)]['surfaceText'])
    start = list(df[df['rel'].apply(lambda e: dict(e)['label'] == relation)]['start'])
    words = [e.replace('[', '').replace(']', '') for e in re.findall("\[+[a-z A-Z]+\]+", str(surface_texts))]
    words = [w.lower().replace('the ', '').replace('a ', '') for w in words]
    words = list(set(words))
    if word in words:
        words.remove(word)
    # words_pos = []
    # for word in words:
    #     for s in start:
    #         if word == s['label'] and len(s['sense_label']) != 0:
    #             words_pos.append([word, s['sense_label']])
    return surface_texts, words

print(conceptnet_request('apple', 'IsA'))