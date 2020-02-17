"""
Evaluate generated descriptions to select the best one based on Rouge measures
"""
# !pip install py-rouge
import rouge
import pandas as pd


def load_desc_data():
    """
    Function to load the description dataset from the Pokedex
    :return: description data in a string
    """
    with open("Data/pokedex_descriptions.txt", "r", encoding="utf8") as file:
        data = file.read().replace("\n", " ")
    return data


def calculate_rouge(description):
    """
    Function to calculate rouge scores up to Rouge5 for one generated description
    :param description: generated description
    :return: rouge scores for generated descriptions as a dict
    """
    evaluator = rouge.Rouge(metrics=['rouge-n'], max_n=5)
    training_data = load_desc_data()
    scores = evaluator.get_scores(description, training_data)
    return scores


def choose_best(df):
    """
    Function to choose the best description based on rouge 1-5 values
    Most favourable: rouge precision of 0 for rouge5, high precision for rouge 2, low precision for rouge4
    :param df: dataframe with description indexes and their rouge scores
    :return: index of best description
    """
    df = df[df.r5 == 0]
    df['r2r4diff'] = df['r2'] - df['r4']
    df['best'] = df['r2r4diff'].idxmax(axis=0)
    return df['best'].iat[0]


def evaluate_descriptions(descriptions):
    """
    Function to evaluate the description, returns the most favourable one
    :param descriptions: list of generated descriptions
    :return: best description
    """
    rouge_scores = []
    for desc in descriptions:
        scores = calculate_rouge(desc)
        rouge_scores.append([descriptions.index(desc), scores['rouge-1']['p'], scores['rouge-2']['p'],
                             scores['rouge-3']['p'], scores['rouge-4']['p'], scores['rouge-5']['p']])
    rouge_scores = pd.DataFrame(rouge_scores, columns=['DescID', 'r1', 'r2', 'r3', 'r4', 'r5'])

    rouge_scores.to_csv('Data/rouge_scores.csv')
    best = descriptions[choose_best(rouge_scores)]
    return best


def check_description_is_novel(description):
    """
    Function to check one description on their rouge scores (if rouge 5 precision is higher than 0)
    :param description: one generated description
    :return: true (if description is novel) or false (if description is not novel)
    """
    scores = calculate_rouge(description)
    if scores['rouge-5']['p'] == 0:
        return True
    else:
        return False
