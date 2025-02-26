from tkinter import *
import pandas as pd
import pygame
from PIL import Image, ImageTk

# ---------------------------- CONVERTERS ---------------------------- #

alphabet_data = pd.read_csv("morse_code_alphabet.csv")
alphabet = {row.letter:row.code for index,row in alphabet_data.iterrows()}
alphabet["\n"] = "\n"
reversed_alphabet = {value:key for key,value in alphabet.items()}

def convert_to_morse():
    global playing
    playing = False
    if pygame.mixer.get_busy():
        pygame.mixer.stop()

    user_input = text_box.get("1.0", "end").rstrip().upper()
    text_to_convert = list(user_input)
    output = []

    try:
        output = [alphabet[letter] for letter in text_to_convert]
    except KeyError:
        error_label["text"] = "Sorry, only letters or numbers."

    if len(output) != 0:
        final_output = ""
        for symbol in output:
            if symbol != "\n":
                final_output += " "
            final_output += symbol
        morse_box.delete("1.0", "end")
        morse_box.insert("1.0", final_output)
        error_label["text"] = ""


def convert_to_text():
    global playing
    playing = False
    if pygame.mixer.get_busy():
        pygame.mixer.stop()

    user_input = morse_box.get("1.0", "end").rstrip()
    morse_lines = user_input.split("\n")
    output = []
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
            error_label["text"] = 'Sorry, only space or the following characters: . - /'

    if len(output) != 0:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "".join(output))
        error_label["text"] = ""


# ------------------------- PLAY AND STOP AUDIO ------------------------- #

playing = False

def play_morse_step(symbol, index, morse_code, dot_sound, dash_sound):
    global playing

    if not playing:
        return

    if pygame.mixer.get_busy():
        error_label["text"] = "Stop the current playback or wait until it ends."
        return

    if symbol == '.':
        dot_sound.play()
    elif symbol == "-":
        dash_sound.play()
    elif symbol == " ":
        pass
    elif symbol == "/":
        pass
    else:
        error_label["text"] = "Sorry, no Morse Code to play."

    if index < len(morse_code):
        window.after(300, play_morse_step, morse_code[index], index+1, morse_code, dot_sound, dash_sound)
    else:
        playing = False


def play_morse():
    global playing
    playing = True

    if pygame.mixer.get_busy():
        error_label["text"] = "Stop the current playback or wait until it ends."
        return

    morse_code = morse_box.get("1.0", "end").rstrip()
    if morse_code == "":
        error_label["text"] = "Sorry, no Morse Code to play."
        playing = False
        return

    morse_code = morse_code.replace("\n", "/")

    pygame.mixer.init()

    dot_sound = pygame.mixer.Sound("dot.wav")
    dash_sound = pygame.mixer.Sound("dash.wav")

    play_morse_step(morse_code[0], 1, morse_code, dot_sound, dash_sound)


def stop_playing():
    global playing
    playing = False
    pygame.mixer.stop()
    error_label["text"] = ""


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

to_morse_button = Button(text="Convert to Morse", command=convert_to_morse, font=(TEXT_FONT, 12, "bold"), bg="SlateGray4", highlightthickness=0)
to_morse_button.grid(column=0, row=4, pady=(5,0), sticky=E, columnspan=2, padx=(0,10))

to_text_button = Button(text="Convert to Text", command=convert_to_text, font=(TEXT_FONT, 12, "bold"), bg="SlateGray4", highlightthickness=0)
to_text_button.grid(column=3, row=4, pady=(5,0), sticky=E)

play_img = Image.open("play_symbol.png")
play_img_resized = play_img.resize((40,40))
play_symbol_img = ImageTk.PhotoImage(play_img_resized)
play_button = Button(image=play_symbol_img, highlightthickness=0, command=play_morse, bg=BG_COLOUR)
play_button.grid(column=2, row=5, sticky=W, padx=(10,0))

play_label_1 = Label(text="Play ", bg=BG_COLOUR, font=(TEXT_FONT, 13), fg="gray13")
play_label_1.grid(column=2, row=5, sticky=E)

play_label_2 = Label(text="Morse Code", bg=BG_COLOUR, font=(TEXT_FONT, 13), fg="gray13")
play_label_2.grid(column=3, row=5, sticky=W)

stop_img = Image.open("stop_symbol.png")
stop_img_resized = stop_img.resize((40,40))
stop_symbol_img = ImageTk.PhotoImage(stop_img_resized)
stop_button = Button(image=stop_symbol_img, highlightthickness=0, command=stop_playing, bg=BG_COLOUR)
stop_button.grid(column=2, row=6, sticky=W, padx=(10,0), pady=(5,0))

stop_label_1 = Label(text="Stop", bg=BG_COLOUR, font=(TEXT_FONT, 13), fg="gray13")
stop_label_1.grid(column=2, row=6, sticky=E)

stop_label_2 = Label(text="Playing", bg=BG_COLOUR, font=(TEXT_FONT, 13), fg="gray13")
stop_label_2.grid(column=3, row=6, sticky=W)

window.grid_columnconfigure(0, weight=4, uniform="equal")  # Mayor tamaño para la columna 0
window.grid_columnconfigure(1, weight=1, uniform="equal")  # Menor tamaño para la columna 1
window.grid_columnconfigure(2, weight=1, uniform="equal")  # Menor tamaño para la columna 2
window.grid_columnconfigure(3, weight=4, uniform="equal")

error_label = Label(text="", bg=BG_COLOUR, font=(TEXT_FONT, 16), fg="gray3")
error_label.grid(column=0, row=7, columnspan=4, pady=(30,20))

window.mainloop()
