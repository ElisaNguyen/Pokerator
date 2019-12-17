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

def get_template(edgetype):
    """
    Method to import the template for description building based on conceptnet edgetype

    :param edgetype: a string that is one of the conceptNet edgetypes
    :return: template for the edgetype that is specified in the excel and expected POS type
    """
    data = pd.read_excel(r'C:\Users\Elisa\PycharmProjects\Pokerator\Data\APNLP_templates.xlsx')
    df = pd.DataFrame(data, columns = ['Edge types', 'Template', 'Expected POS'])
    templates = df.values.tolist()
    for t in templates:
        if t[0] == edgetype:
            return t[1], t[2]

def get_random_edgetype():
    """
    Method to get random edgetype

    :return: a random edgetype as a string
    """
    return str(random.choice(cn.get_all_relations()))

def choose_word_pos(word_list, pos_list):
    '''
    Method to choose one word/characteristic out of the word list received from conceptnet
    Based on POS tagging of the root of the sentence (dependency parsing) and the expected POS tag
    :param word_list: word list from conceptnet
    :param pos_list: from excel, expected pos for the requested sentence
    :return: one word/characteristic out of word list that fits to the expected pos tag
    '''
    word_list_possible = []
    nlp = spacy.load('en_core_web_sm')
    for characteristic in word_list:
        doc = nlp(characteristic)
        for token in doc:
            if token.dep_ == "ROOT":
                for tag in pos_list:
                    if token.pos_ == tag:
                        word_list_possible.append(characteristic)
    return random.choice(word_list_possible)

def build_sentence(word):
    """
    Method to write a sentence given a word

    :param word: a word which was one of the answers given by the user
    :return: a sentence as string
    """
    cn_answer = cn.conceptnet_request(word)
    t = str(get_template(cn_answer[1])[0])
    word_list = cn_answer[0]
    chosen_word = choose_word_pos(word_list, str(get_template(cn_answer[1])[1]).split(','))
    sentence = t.replace(t[t.find("<"):t.find(">")+1], chosen_word) + ". "
    return sentence

def build_description(answers):
    """
    Method to write the description of the Pokemon, randomly select 2 sentences

    :param answers: list of answers given by user that are used for the name
    :return: a description as string
    """
    description = ""
    for i in range(2):
        answer = random.choice(answers)
        answers.remove(answer)
        description = description + build_sentence(answer.lower())
    return description

print(build_description(["penguin", "tulip"]))
