# if code does not work run these lines in the command line:
#!pip install  -q gpt-2-simple
#!python -m spacy download en_core_web_sm

from NameEvaluation import evaluation_name
from PokedexEntryBuilder import build_description
from QuestionHandling import ask_questions, select_answers
from Wordblender import blend_a_word
import warnings
warnings.filterwarnings("ignore")


if __name__== "__main__":
    # evaluate two longest words
    answers = ask_questions()
    print('Your Pokémon is now being generated...')
    w1, w2 = select_answers(list(answers.values()))
    blended_words = blend_a_word(w1, w2)
    pokemon = evaluation_name(blended_words)
    description = build_description([w1, w2], pokemon)

    print(pokemon.upper())
    print('-------------------------------------------')
    print(description)
