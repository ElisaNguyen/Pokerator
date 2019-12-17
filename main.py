import NameEvaluation as ne
import Wordblender as wb

if __name__== "__main__":
    words = wb.blend_a_word("teapot", "horse")
    ne.run(words)