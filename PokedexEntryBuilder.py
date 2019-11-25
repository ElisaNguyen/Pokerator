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

def conceptnet_request(word):
    """

    :param word:
    :return:
    """
    #random from list of relations
    #api call
    pass
