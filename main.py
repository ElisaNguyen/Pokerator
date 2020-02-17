# if code does not work run these lines in the command line:
#!pip install  -q gpt-2-simple
#!pip install pyspellchecker
#!python -m spacy download en_core_web_sm

from NameEvaluation import evaluation_name
from PokedexEntryBuilder import build_description
from QuestionHandling import ask_questions
from Wordblender import blend_a_word
from DescriptionEvaluation import check_description_is_novel
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__== "__main__":
    # evaluate two longest words
    #answers = ask_questions()
    answers = ['soup', 'march', 'whale', 'hibiskus', 'red']
    print('The egg is hatching...')
    blended_words, w1, w2 = blend_a_word(answers)
    pokemon = evaluation_name(blended_words)
    while True:
        description = build_description([w1, w2], pokemon, 'run750')
        if check_description_is_novel(description):
            break
    print(pokemon.upper())
    print('-------------------------------------------')
    print(description)