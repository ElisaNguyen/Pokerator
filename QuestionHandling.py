"""
Ask questions to the user and get their responses.
Questions are stored in APNLP_QuestionsToUser.xlsx
"""
import pandas as pd


# method that returns questions to ask to the user in list format
def get_questions():
    '''
    Method to get all questions out of the excel

    :return: questions in list format
    '''
    data = pd.read_excel('Data/APNLP_QuestionsToUser.xlsx')
    df = pd.DataFrame(data, columns=['Questions'])
    list = df.values.tolist()
    questions = []
    for q in list:
        q = str(q)[2:-2]
        questions.append(q)
    return questions


# Method to ask questions to user and return the answers
def ask_questions():
    '''
    Method to ask questions to users

    :return: dictionary of question and answer pairs, with the questions as keys
    '''
    answers = {}
    for q in get_questions():
        answers[str(q)] = input(q)
    return answers


def select_answers(answers):
    answers = answers[2:]
    print(answers)
    return sorted(answers, key=len)[-2:]



