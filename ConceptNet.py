import requests
import pandas as pd
import re


def conceptnet_request(word, relation):
    """
    Send an API request to conceptNet for a word and for a certain realtion with the word the surface text in which it
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
    words = [e.replace('[', '').replace(']', '') for e in re.findall("\[+[a-z A-Z]+\]+", str(surface_texts))]
    words = list(set(words))
    remove = []
    for w in words:
        if word in w:
            remove.append(w)
    [words.remove(w) for w in remove]
    return surface_texts, words