import NameEvaluation as ne
from QuestionHandling import ask_questions, select_answers
from Wordblender import blend_a_word

if __name__== "__main__":
    answers = ask_questions()
    w1, w2 = select_answers(list(answers.values()))
    blended_words = blend_a_word(w1, w2)

    answers = answers[2:]
