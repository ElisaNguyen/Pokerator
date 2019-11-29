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
import requests
import re
import numpy as np

#Method to import the template for description building based on conceptnet edgetype
def get_template(edgetype):
    data = pd.read_excel(r'Data\APNLP_templates.xlsx')
    df = pd.DataFrame(data, columns = ['Edge types', 'Template'])
    templates = df.values.tolist()
    for t in templates:
        if t[0] == edgetype:
            return t[1]

#Method for requesting the word and relation(edgetype) from conceptnet.
#To be outsourced to new tool-file
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

#Method to write the description of the Pokemon, randomly select 2 sentences
def build_description(answers):
    #random generator in range of len(answers) to take the random answer to base the description on
    #afterwards delete that answer from the answers list
    #do the random thing again
    #build the description
    description = "test"
    return description