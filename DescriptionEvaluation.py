"""
Evaluate generated descriptions to select the best one based on Rouge measures
"""
# !pip install py-rouge
import rouge


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
    :return: rouge scores for generated descriptions
    """
    evaluator = rouge.Rouge(metrics=['rouge-n'], max_n=5)
    training_data = load_desc_data()
    scores = evaluator.get_scores(description, training_data)
    return scores
print(calculate_rouge("It is said that whoever it is that desires it must embrace it. It is said to keep it close by "
                      "bending its branches to its waist. Its two tails dance through the air with each passing "
                      "second."))


def evaluate_descriptions(descriptions):
    """
    Function to evaluate the description, returns the most favourable one
    Most favourable: rouge scores of 0 for rouge5, high scores for rouge1 and rouge 2, low score for rouge4
    :param descriptions: list of generated descriptions
    :return: best description
    """
