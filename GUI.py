# #DISCLAIMER: STILL UNDER CONSTRUCTION
#
# #User Interface
# #https://likegeeks.com/python-gui-examples-tkinter-tutorial/
# from tkinter import *
#
#
# def submit(answers):
#     for answer in answers:
#         print(answers.get())
#
# #Method to build the GUI, expects questions in dictionary form as input
# def build_GUI(questions):
#     window = Tk()
#     window.geometry('350x200')
#     window.title('Pokérator')
#
#     lbl = Label(window, text="Pokérator - Unveil your inner Pokémon", font=("Arial Bold", 15))
#     lbl.grid(column=0, row=0)
#
#     answers = []
#     for i in range(len(questions)):
#         qtxt = Label(window, text=str(list(questions.keys())[i]), font=("Arial", 11))
#         qtxt.grid(column=0, row=10+i)
#         answer = Entry(window, width=10)
#         answers.append(answer)
#         answer.grid(column=2, row=10+i)
#
#     btn = Button(window, text="Submit", command=submit(answers))
#     btn.grid(column=0, row=30)
#     window.mainloop()
#
# qs= {"What?": "a", "Why?": "b"}
# build_GUI(qs)