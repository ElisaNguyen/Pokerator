"""Look up words in conceptNet (using a GET command to the REST API)
Randomly (?) choose relations (e.g. CapableOf), test first if relation available
E.g. http://conceptnet.io/c/en/horse?rel=/r/CapableOf&limit=10
Generate pokedex entry
Create templates for every relation (siehe Bild)
E.g. CapableOf → Name can … It...
Insert conceptnet response into template
E.g. Horsemon can jump a barrier.
Adjust grammar if necessary?
"""
import pandas as pd
import random
import ConceptNet as cn
import spacy
from spellchecker import SpellChecker
import gpt_2_simple as gpt2
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['KMP_WARNINGS'] = 'off'


def get_template(edgetype):
    """
    Method to import the template for description building based on conceptnet edgetype

    :param edgetype: a string that is one of the conceptNet edgetypes
    :return: template for the edgetype that is specified in the excel and expected POS type
    """
    xls = pd.ExcelFile('Data\APNLP_templates.xlsx')
    df = pd.read_excel(xls, edgetype)
    templates = df.values.tolist()
    chosen_t = random.choice(templates)
    return chosen_t[0], chosen_t[1]


def get_random_edgetype():
    """
    Method to get random edgetype

    :return: a random edgetype as a string
    """
    return str(random.choice(cn.get_all_relations()))


def filter_word_pos(word_list, pos_list):
    """
    Method to choose one word/characteristic out of the word list received from conceptnet
    Based on POS tagging of the root of the sentence (dependency parsing) and the expected POS tag
    :param word_list: word list from conceptnet
    :param pos_list: from excel, expected pos for the requested sentence in list form
    :return: list of characteristics out of word list that fits to the expected pos tag
    """
    word_list_possible = []
    nlp = spacy.load('en_core_web_sm')
    for characteristic in word_list:
        doc = nlp(characteristic)
        for token in doc:
            if token.dep_ == "ROOT":
                for tag in pos_list:
                    if token.pos_ == tag:
                        word_list_possible.append(characteristic)
    return word_list_possible


def check_spelling(word):
    """
    Method to check whether a word is spelled correctly and returns the most likely word if its mispelled based on the minimum edit distance
    :param word: a word (answer by user)
    :return: correctly spelled word
    """
    spell = SpellChecker()
    mispelled = spell.unknown([word])
    if len(mispelled) > 0:
        return spell.correction(word)
    else:
        return word


def build_sentence(word):
    """
    Method to write a sentence given a word, it looks up all the answers from conceptnet to find a fitting one

    :param word: a word which was one of the answers given by the user
    :return: a sentence as string
    """
    cn_answer = cn.conceptnet_request(check_spelling(word))
    edges = cn_answer[1]
    random.shuffle(edges)
    for edge in edges:
        t = str(get_template(edge)[0])
        word_list = cn_answer[0][edge]
        possible_words = filter_word_pos(word_list, str(get_template(edge)[1]).split(','))
        if len(possible_words) > 0:
            chosen_word = random.choice(possible_words)
            sentence = t.replace(t[t.find("<"):t.find(">") + 1], chosen_word) + ". "
            return sentence


def build_description(answers, name):
    """
    Method to write the description of the Pokemon, randomly select 2 sentences

    :param answers: list of answers given by user that are used for the name
    :param name: name of the pokemon
    :return: a description as string
    """
    answer = random.choice(answers)
    description = build_sentence(answer.lower())
    if description is None:
        description = name.capitalize()
    description = generation_gtp2(description, name)
    return description


def filter_pokemon_names(desc, name):
    """
    Filters out the Pokemon names in the description generated by the model.

    :param desc: generated description
    :param name: name of the Pokemon
    :return: description without other Pokemon names
    """
    poks = pd.read_csv('Data/pokemon.csv')
    for pok in poks['name']:
        desc = desc.replace(pok, name.capitalize())
    return desc


def generation_gtp2(input_sent, name):
    """
    Generates a longer description based on the input sentence from concept net. It uses the gtp2 model trained on
    real Pokedex entries.

    :param input_sent: input senteence from ConceptNet
    :param name: name of the Pokemon
    :return: the description for the Pokemon
    """
    input_sent += ' '
    sess = gpt2.start_tf_sess()
    try:
        gpt2.load_gpt2(sess, run_name='run3')
    except:
        gpt2.download_gpt2()
        gpt2.load_gpt2(sess, run_name='run3')
    desc = gpt2.generate(sess, run_name='run3', length=30, prefix=input_sent, return_as_list=True)[0]
    desc = filter_pokemon_names(desc, name)
    desc = desc.replace('. ', '.')
    desc = '.\n'.join(desc.split('.')[:-1]) + '.'
    desc = desc.replace('  ', ' ').replace('\n ', '\n')
    return desc
