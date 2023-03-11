import tkinter
import random
import pandas
import json
import os

# declaring my my dictionary, that all my files will be added into
english_french_dict = {}
french_word = None
try:
    # if csv file exist, we will load it into the english_french_dict dictionary
    if os.path.getsize("words_to_learn.csv") == 0:
        file1 = open("words_to_learn.csv", "r")
        english_french_dict = json.load(file1)
except FileNotFoundError:
    # if it does not exist, we are creating a new file
        data = open("words_to_learn.csv", "w")
        json.dump(english_french_dict, data, indent=4)

# creating a function that will save the updated english_french_dict to the words_to_learn csv file
def save_data():
   data = open("words_to_learn.csv", "w")
   json.dump(english_french_dict, data, indent=4)

# grabs a random set of words from english_french_dict and assigns them to the canvas
# also sets the countdown function, so it switches the color backround after 3 seconds
def display_words_on_screen():
    global french_word
    random_pair = random.choice(list(english_french_dict.items()))
    french_word = random_pair[0]
    english_word = random_pair[1]
    canvas.itemconfig(display_word, text=french_word)
    canvas.itemconfig(language_display, text="French")
    count_down(4, english_word, )

# grabs all data from the french_words.csv files and converts it into a diction that only contains english and french workds
def convert_cvs_file_dict():
    english_french_data_list = pandas.read_csv("./data/french_words.csv")
    english_list = english_french_data_list.to_dict("list")["English"]
    french_list = english_french_data_list.to_dict("list")["French"]
    num = 0
    for word in english_list:
        english_french_dict.update({french_list[french_list.index(french_list[num])]: word})
        num += 1
    return english_french_dict

# creates front card photo and assigns convert_cvs_file_dict to english_french_dict
def generate_random_english_french_pair():
    global english_french_dict
    global french_word
    canvas.itemconfig(card_photo, image=card_front_photo)
    english_french_dict = convert_cvs_file_dict()
    display_words_on_screen()

#removes french/english word from enlish_french_dict. creates front photo, and displays words on screens
def remove_card_from_list():
    global english_french_dict, french_word
    canvas.itemconfig(card_photo, image=card_front_photo)
    english_french_dict = convert_cvs_file_dict()
    del english_french_dict[french_word]
    display_words_on_screen()
    save_data()

# creates a countown for 3 seconds and then flops the card
def count_down(timer, english_word):
    timer -= 1
    if timer != 0:
        window.after(1000, count_down, timer, english_word)
    if timer == 0:
        canvas.itemconfig(display_word, text=english_word)
        canvas.itemconfig(language_display, text="English")
        canvas.itemconfig(card_photo, image=card_back_photo)
    if timer > 0:
        window.after_cancel(window.after(1000, count_down, timer, english_word))


## UI Setup

window = tkinter.Tk()
window.config(bg="#b1dec5", pady=50, padx=50)
window.title("Flash Card")
card_front_photo = tkinter.PhotoImage(file="images/card_front.png")
card_back_photo = tkinter.PhotoImage(file="images/card_back.png")
canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg="#b1dec5")
card_photo = canvas.create_image(400, 263, image=card_front_photo)
language_display = canvas.create_text(400, 131, fill="black", anchor="center", width=800, font=("Ariel", 36))
display_word = canvas.create_text(400, 263,  fill="black", anchor="center", width=800, font=("Ariel", 48, "bold"))
canvas.grid(column=0, row=0,columnspan=2, pady=50, padx=50 )
right_button_image = tkinter.PhotoImage(file="./images/right.png")
right_button = tkinter.Button(command=remove_card_from_list,  highlightbackground="#b1dec5", image=right_button_image)
right_button.grid(column=1, row=1)
wrong_button_image = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(bg="#b1dec5", command=generate_random_english_french_pair, highlightthickness=0, image=wrong_button_image)
wrong_button.grid(column=0, row=1, padx=50)
generate_random_english_french_pair()
# if the user knows every word, they win the game
if len(english_french_dict) == 0:
    canvas.itemconfig(display_word, text="You have won the game")
    window.destroy()
window.mainloop()

