from NameEvaluation import run
from PokedexEntryBuilder import build_description
from QuestionHandling import ask_questions, select_answers
from Wordblender import blend_a_word

if __name__== "__main__":
    # evaluate two longest words
    # answers = ask_questions()
    # w1, w2 = select_answers(list(answers.values()))
    # blended_words = blend_a_word(w1, w2)
    # pokemon = run(blended_words)
    # description = build_description([w1, w2])
    # print(pokemon)
    # print(description)

    # evaluate all answers
    answers = ask_questions()
    blended_words = dict()
    for w1 in answers:
        for w2 in answers:
            if w1 != w2:
                words = blend_a_word(w1, w2)
                for w in words:
                    blended_words[w] = [w1, w2]
    pokemon = run(blended_words.keys())
    description = build_description(blended_words[pokemon])
    print('Your Pokémon: ')
    print(pokemon)
    print(description)
