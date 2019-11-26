"""
Ask questions to the user and get their responses.
Questions are stored in APNLP_QuestionsToUser.xlsx
"""
import pandas as pd

#method that returns questions to ask to the user in list format
def get_questions():
    data = pd.read_excel(r'Data\APNLP_QuestionsToUser.xlsx')
    df = pd.DataFrame(data, columns=['Questions'])
    questions = df.values.tolist()
    return questions

#Method to ask questions to user and return the answers
def ask_questions():
    answers = {}
    for q in get_questions():
        answers[str(q)] = input (q)
    return answers




