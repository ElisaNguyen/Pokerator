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
    with open("Data\pokedex_descriptions.txt", "r", encoding="utf8") as file:
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
    Most favourable: rouge precision of 0 for rouge5, high precision for rouge1 and rouge 2, low precision for rouge4
    :param df: dataframe with description indexes and their rouge scores
    :return: index of best description
    """
    print(df)
    df = df[df.r5 > 0]
    df_rank = pd.DataFrame()
    df_rank['r1_rank'] = df['r1'].rank()
    df_rank['r2_rank'] = df['r2'].rank()
    df_rank['r4_rank'] = df['r4'].rank()
    #make the sum of the ranks and choose the highest rank overall
    #df_rank['final_rank'] = df_rank.sum()
    print(df_rank)
    best = 1
    return best


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
    best = descriptions[choose_best(rouge_scores)]
    return best

evaluate_descriptions(["It is said that whoever it is that desires it must embrace it. It is said to keep it close by "
                       "bending its branches to its waist. Its two tails dance through the air with each passing "
                       "second.",
                       "It tries to eat anything that moves. The pattern on this Pokémon's wings suggests that it may "
                       "have come into being as a result of living with water. When it swims by spinning its "
                       "tentacles, it swallows everything in one big gulp.", "Walmart's cubby loves to eat at the "
                                                                             "bustling stands of fast-food "
                                                                             "restaurants,  and shares a snack with "
                                                                             "its companions. Teaapple's thin and "
                                                                             "flexible body lets it bend and sway to "
                                                                             "avoid any attack, however strong it may "
                                                                             "be. From its mouth, this Pokémon spits "
                                                                             "a corrosive fluid that melts even "
                                                                             "iron."])
