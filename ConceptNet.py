import requests
import pandas as pd
import re
import random

def get_all_relations():
    """
    Method to return all relations of conceptnet specified in the xlsx

    :return: List of all relations, as strings
    """
    data = pd.read_excel(r'C:\Users\Elisa\PycharmProjects\Pokerator\Data\APNLP_templates.xlsx')
    df = pd.DataFrame(data, columns = ['Edge types'])
    edgetypes = df.values.tolist()
    relations = []
    for e in edgetypes:
        relations.append(str(e)[2:-2])
    return relations

def conceptnet_request(word):
    """
    Send an API request to conceptNet for a word and for a certain relation with the word the surface text in which it
    can be used and the related words.

    :param word: a word
    :return: list of words to a given relation, that relation, and the surface texts from conceptnet
    """
    url = 'http://api.conceptnet.io/c/en/' + word + '?limit=100'
    print(url)
    response = requests.get(url).json()
    df = pd.DataFrame(response['edges'])
    unique_edges = df['rel'].apply(lambda e: dict(e)['label']).unique()
    possible_edges = [value for value in unique_edges if value in get_all_relations()]
    chosen_edge = random.choice(possible_edges)
    surface_texts = list(df[df['rel'].apply(lambda e: dict(e)['label'] == chosen_edge)]['surfaceText'])
    words = [e.replace('[', '').replace(']', '') for e in re.findall("\[+[a-z A-Z]+\]+", str(surface_texts))]
    words = [w.lower().replace('the ', '').replace('a ', '') for w in words]
    words = list(set(words))
    if word in words:
        words.remove(word)
    return words, chosen_edge, surface_texts
