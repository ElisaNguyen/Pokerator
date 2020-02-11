"""
Evaluate generated descriptions to select the best one based on Rouge measures
"""
# !pip install rouge
import rouge


def load_desc_data():
    """
    Function to load the description dataset from the Pokedex
    :return: description data in a string
    """
    with open("Data\pokedex_descriptions.txt", "r", encoding="utf8") as file:
        data = file.read().replace("\n", " ")
    return data


def calculate_rouge(descriptions):
    """
    Function to calculate rouge scores up to Rouge5 for generated descriptions
    :param descriptions: generated descriptions
    :return: rouge scores for generated descriptions
    """


def evaluate_descriptions(descriptions):
    """
    Function to evaluate the description, returns the most favourable one
    Most favourable: rouge scores of 0 for rouge5, high scores for rouge1 and rouge 2, low score for rouge4
    :param descriptions: list of generated descriptions
    :return: best description
    """
