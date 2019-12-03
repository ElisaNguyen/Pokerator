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

def get_template(edgetype):
    """
    Method to import the template for description building based on conceptnet edgetype

    :param edgetype: a string that is one of the conceptNet edgetypes
    :return: template for the edgetype that is specified in the excel
    """
    data = pd.read_excel(r'C:\Users\Elisa\PycharmProjects\Pokerator\Data\APNLP_templates.xlsx')
    df = pd.DataFrame(data, columns = ['Edge types', 'Template'])
    templates = df.values.tolist()
    for t in templates:
        if t[0] == edgetype:
            return t[1]

def get_random_edgetype():
    """
    Method to get random edgetype

    :return: a random edgetype as a string
    """
    data = pd.read_excel(r'C:\Users\Elisa\PycharmProjects\Pokerator\Data\APNLP_templates.xlsx')
    df = pd.DataFrame(data, columns = ['Edge types'])
    edgetypes = df.values.tolist()
    return str(random.choice(edgetypes))[2:-2]

def build_sentence(word, relation):
    """
    Method to write a sentence given a word and a relation

    :param word: a word which was one of the answers given by the user
    :param relation: a relation (same as edgetype) from conceptnet
    :return: a sentence as string
    """
    t = str(get_template(relation))
    r = cn.conceptnet_request(word, relation)
    if len(r[1]) == 0:
        r = cn.conceptnet_request(word, "AtLocation")
    sentence = t.replace(t[t.find("<"):t.find(">")+1], str(r[1][0])) + ". "
    return sentence

def build_description(answers):
    """
    Method to write the description of the Pokemon, randomly select 2 sentences

    :param answers: list of answers given by user
    :return: a description as string
    """
    description = ""
    for i in range(2):
        answer = random.choice(answers)
        answers.remove(answer)
        relation = get_random_edgetype()
        description = description + build_sentence(answer, relation)
    return description