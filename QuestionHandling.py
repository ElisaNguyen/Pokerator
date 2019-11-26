"""
Ask questions to the user and get their responses.
Questions are stored in APNLP_QuestionsToUser.xlsx
"""
import pandas as pd

#method that returns questions to ask to the user in a dictionary format
def get_questions():
    data = pd.read_excel(r'Data\APNLP_QuestionsToUser.xlsx')
    questions = pd.DataFrame(data, columns=['Questions'])
    return questions

