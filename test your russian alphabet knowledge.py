import tkinter as tk
from pygame import mixer
from random import choice, shuffle, randint
from threading import Thread
from time import sleep

def play_sound(letra):
    mixer.init()
    v = randint(0, 3)
    mixer.music.load(f"audios/{letra[0]}{letra[1]}({v}).mp3")
    Thread(target=lambda: mixer.music.play()).start()

def check_answer(wind, button, correct_letter):
    if button.cget("text") in correct_letter:
        button.config(bg="green")

        wind.update_idletasks()
        sleep(0.5)

        for widget in wind.winfo_children():
            widget.destroy()

        new_window()

    else:
        button.config(bg="red")
        wind.update_idletasks()
        wind.after(500, button.config(bg="SystemButtonFace"))

def new_window():
    global letters
    global base
    global window
    global size

    if len(letters) == 0:
        letters = base.copy()

    chosen_letter = choice(letters)
    letters.remove(chosen_letter)

    options = base.copy()
    shuffle(options)

    window.update_idletasks()

    button_font = 22
    button_height = 1
    button_width = 3

    playsoundagin = tk.Button(window, text="Replay the audio", font=("Arial", 15), command=lambda: play_sound(chosen_letter))
    playsoundagin.place(x=size/2, y=25, anchor="n")
    window.update_idletasks()

    n = playsoundagin.winfo_y() + playsoundagin.winfo_height() + 25

    buttons = []

    # Create 11 buttons (from 1 to 11).
    b1 = tk.Button(window, text=choice(options[0]), font=("Arial", button_font), width=button_width, height=button_height, command=lambda: check_answer(window, b1, chosen_letter))
    b1.place(x=14, y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b1)

    x = b1.winfo_x() + b1.winfo_width()
    espaco = 0
    for i in range(1, 11):
        button = tk.Button(window, text=choice(options[i]), font=("Arial", button_font), width=button_width, height=button_height,
                        command=lambda b=i: check_answer(window, buttons[b], chosen_letter))
        button.place(x=x, y=n, anchor="nw")
        
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width() + espaco

    n = b1.winfo_y() + b1.winfo_height()

    # Create 11 buttons (from 12 to 33).
    b12 = tk.Button(window, text=choice(options[11]), font=("Arial", button_font), width=button_width, height=button_height, command=lambda: check_answer(window, b12, chosen_letter))
    b12.place(x=b1.winfo_x(), y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b12)

    x = b12.winfo_x() + b12.winfo_width()
    espaco = 0
    for i in range(12, 22):
        button = tk.Button(window, text=choice(options[i]), font=("Arial", button_font), width=button_width, height=button_height,
                        command=lambda b=i: check_answer(window, buttons[b], chosen_letter))
        button.place(x=x, y=n, anchor="nw")
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width() + espaco

    n = b12.winfo_y() + b12.winfo_height()

    # Create 11 buttons (from 23 to 33).
    b23 = tk.Button(window, text=choice(options[22]), font=("Arial", button_font), width=button_width, height=button_height, command=lambda: check_answer(window, b23, chosen_letter))
    b23.place(x=b1.winfo_x(), y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b23)

    x = b23.winfo_x() + b23.winfo_width()
    espaco = 0
    for i in range(23, 33):
        button = tk.Button(window, text=choice(options[i]), font=("Arial", button_font), width=button_width, height=button_height,
                        command=lambda b=i: check_answer(window, buttons[b], chosen_letter))
        button.place(x=x, y=n, anchor="nw")
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width() + espaco

    # Play the sound after the buttons have loaded in the window.
    play_sound(chosen_letter)

    # Start window loop
    window.mainloop()

global base

base = [["А", "а"], ["Б", "б"], ["В", "в"], ["Г", "г"], ["Д", "д"], ["Е", "е"], ["Ё", "ё"], ["Ж", "ж"], ["З", "з"], ["И", "и"], ["Й", "й"],
          ["К", "к"], ["Л", "л"], ["М", "м"], ["Н", "н"], ["О", "о"], ["П", "п"], ["Р", "р"], ["С", "с"], ["Т", "т"], ["У", "у"], ["Ф", "ф"],
          ["Х", "х"], ["Ц", "ц"], ["Ч", "ч"], ["Ш", "ш"], ["Щ", "щ"], ["Ъ", "ъ"], ["Ы", "ы"], ["Ь", "ь"], ["Э", "э"], ["Ю", "ю"], ["Я", "я"]]

global letters
letters = base.copy()

global window

window = tk.Tk()
window.title("Learn Russian Alphabet")

global size
size = 700
pos_x = (window.winfo_screenwidth() // 2) - (size // 2)
pos_y = (window.winfo_screenheight() // 2) - ((size - 200) // 2)

window.geometry(f"{size}x{280}+{pos_x}+{pos_y}")
window.resizable(False, False)

new_window()
