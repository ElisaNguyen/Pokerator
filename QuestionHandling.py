"""
Ask questions to the user and get their responses.
Questions are stored in APNLP_QuestionsToUser.xlsx
"""
import pandas as pd


def get_questions():
    """
    Method to get all questions out of the excel

    :return: questions in list format
    """
    data = pd.read_excel('Data/APNLP_QuestionsToUser.xlsx')
    df = pd.DataFrame(data, columns=['Questions'])
    lst = df.values.tolist()
    questions = []
    for q in lst:
        q = str(q)[2:-2]
        questions.append(q)
    return questions


def ask_questions():
    """
    Method to ask questions to users

    :return: list of answers
    """
    answers = []
    for q in get_questions():
        while True:
            try:
                answer = input(q)
                if " " in answer:
                    raise ValueError
                answers.append(answer)
                break
            except ValueError:
                print("Invalid answer. Please answer in only one word! :)")
    return answers


