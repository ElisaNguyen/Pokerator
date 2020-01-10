"""
Ask questions to the user and get their responses.
Questions are stored in APNLP_QuestionsToUser.xlsx
"""
import pandas as pd


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


def ask_questions():
    """
    Method to ask questions to users

    :return: dictionary of question and answer pairs, with the questions as keys
    """
    answers = {}
    for q in get_questions():
        while True:
            try:
                answer = input(q)
                if " " in answer:
                    raise ValueError
                answers[str(q)] = answer
                break
            except ValueError:
                print("Invalid answer. Please answer in only one word! :)")
    return answers


def select_answers(answers):
    """
    Selects the two longest words of the answers and returns them.

    :param answers: list of given answers
    :return: two longest answers without the first two
    """
    answers = answers[2:]
    return sorted(answers, key=len)[-2:]



