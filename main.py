from tkinter import *
import pandas as pd

# ---------------------------- CONVERTERS ---------------------------- #

alphabet_data = pd.read_csv("morse_code_alphabet.csv")
alphabet = {row.letter:row.code for index,row in alphabet_data.iterrows()}
alphabet["\n"] = "\n"
reversed_alphabet = {value:key for key,value in alphabet.items()}

def convert_to_morse():
    user_input = text_box.get("1.0", "end").rstrip().upper()
    text_to_convert = list(user_input)
    output = []
    error = ""

    try:
        output = [alphabet[letter] for letter in text_to_convert]
    except KeyError:
        error = "Sorry, only letters or numbers, please."

    if len(output) != 0:
        morse_box.delete("1.0", "end")
        morse_box.insert("1.0", " ".join(output))
        error_label["text"] = ""

    error_label["text"] = error


def convert_to_text():
    user_input = morse_box.get("1.0", "end").rstrip()
    morse_lines = user_input.split("\n")
    output = []
    error = ""
    for line in morse_lines:
        try:
            morse_words = line.split("/")
            word_output = []
            for word in morse_words:
                morse_letters = word.split(" ")
                letter_output = [reversed_alphabet[code] for code in morse_letters if code != ""]
                word_output.append("".join(letter_output))
                word_output.append(" ")
            output.append("".join(word_output))
            output.append("\n")
        except KeyError:
            error = 'Sorry, only ".", "-", "/" or " ", please.'

    if len(output) != 0:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "".join(output))
        error_label["text"] = ""

    if error:
        error_label["text"] = error


# ---------------------------- UI SETUP ------------------------------- #

TITLE_FONT = "Agency FB"
TEXT_FONT = "@Microsoft JhengHei UI"
BG_COLOUR = "SlateGray3"

window = Tk()
window.title("Text to Morse Code Converter")
window.config(padx=110, pady=50, bg=BG_COLOUR)

canvas = Canvas(width=200, height=70, bg=BG_COLOUR, highlightthickness=0)
telegraph_img = PhotoImage(file="telegraph_thin.png")
canvas.create_image(100, 35, image=telegraph_img)
canvas.grid(column=1, row=0, columnspan=2, pady=0)

title_left = Label(text="TEXT TO MORSE", font=(TITLE_FONT, 64, "normal"), bg=BG_COLOUR, fg="black")
title_left.grid(column=0, row=0, sticky=N+S+E, pady=0)

title_right = Label(text="MORSE TO TEXT", font=(TITLE_FONT, 64, "normal"), bg=BG_COLOUR, fg="black")
title_right.grid(column=3, row=0, sticky=N+S+W, pady=0)

title_middle = Label(text="CONVERTER", font=(TITLE_FONT, 35, "normal"), bg=BG_COLOUR, fg="black")
title_middle.grid(column=1, row=1, sticky=N+W+E, columnspan=2, pady=(0,60))

input_text_label = Label(text="Write or Paste your Text:", bg=BG_COLOUR, font=(TEXT_FONT, 16))
input_text_label.grid(column=0, row=2, sticky=W, columnspan=2)

input_morse_label = Label(text="Write or Paste your Morse Code:", bg=BG_COLOUR, font=(TEXT_FONT, 16))
input_morse_label.grid(column=2, row=2, sticky=W, columnspan=2, padx=(10,0))

text_box = Text(height=5, width=30, font=(TEXT_FONT, 16))
text_box.focus()
text_box.grid(column=0, row=3, sticky=W+E, columnspan=2, padx=(0,10))

morse_box = Text(height=5, width=30, font=(TEXT_FONT, 16))
morse_box.grid(column=2, row=3, sticky=W+E, columnspan=2, padx=(10,0))

to_morse_button = Button(text="Convert to Morse", command=convert_to_morse, font=(TEXT_FONT, 12, "bold"), bg="SlateGray4")
to_morse_button.grid(column=0, row=4, pady=(5,0), sticky=E, columnspan=2, padx=(0,10))

to_text_button = Button(text="Convert to Text", command=convert_to_text, font=(TEXT_FONT, 12, "bold"), bg="SlateGray4")
to_text_button.grid(column=3, row=4, pady=(5,0), sticky=E)

error_label = Label(text="", bg=BG_COLOUR, font=(TEXT_FONT, 16), fg="gray3")
error_label.grid(column=0, row=5, columnspan=4, pady=(10,40))

window.mainloop()
