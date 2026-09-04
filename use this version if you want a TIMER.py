import tkinter as tk
from pygame import mixer
from random import choice, shuffle, randint
from threading import Thread


def play_sound(letra):
    mixer.init()

    # Para o áudio anterior
    mixer.music.stop()

    v = randint(0, 3)
    mixer.music.load(f"audios/{letra[0]}{letra[1]}({v}).mp3")
    mixer.music.play()


def next_letter():
    global timer_id
    global contador_id

    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None

    if contador_id is not None:
        window.after_cancel(contador_id)
        contador_id = None

    for widget in window.winfo_children():
        widget.destroy()

    new_window()


def check_answer(wind, button, correct_letter):
    global timer_id
    global contador_id

    if button.cget("text") in correct_letter:
        button.config(bg="green")

        if timer_id is not None:
            wind.after_cancel(timer_id)
            timer_id = None

        if contador_id is not None:
            wind.after_cancel(contador_id)
            contador_id = None

        wind.after(500, next_letter)

    else:
        button.config(bg="red")

        wind.after(
            500,
            lambda: button.config(bg="SystemButtonFace")
        )

def atualizar_timer():
    global tempo_restante
    global contador_id
    global timer_label

    tempo_restante -= 100

    if tempo_restante <= 0:
        timer_label.config(text="0.0")
        contador_id = None
        return

    segundos = tempo_restante / 1000
    timer_label.config(text=f"{segundos:.1f}")

    contador_id = window.after(100, atualizar_timer)   

def new_window():
    global letters
    global window
    global size
    global timer_id
    global contador_id
    global tempo_restante
    global timer_label

    if len(letters) == 0:
        letters = base.copy()

    chosen_letter = choice(letters)
    letters.remove(chosen_letter)

    options = base.copy()
    shuffle(options)

    button_font = 22
    button_height = 1
    button_width = 3

    playsoundagin = tk.Button(
        window,
        text="Replay the audio",
        font=("Arial", 15),
        command=lambda: play_sound(chosen_letter)
    )

    playsoundagin.place(
        x=size / 2,
        y=25,
        anchor="n"
    )

    window.update_idletasks()

    n = playsoundagin.winfo_y() + playsoundagin.winfo_height() + 25

    buttons = []

    timer_label = tk.Label(
        window,
        text="3.0",
        font=("Arial", 20)
    )

    timer_label.place(
        x=size - 30,
        y=25,
        anchor="ne"
    )

    # Primeira linha
    b1 = tk.Button(
        window,
        text=choice(options[0]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window, b1, chosen_letter
        )
    )

    b1.place(x=14, y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b1)

    x = b1.winfo_x() + b1.winfo_width()

    for i in range(1, 11):
        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window, buttons[b], chosen_letter
            )
        )

        button.place(x=x, y=n, anchor="nw")
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width()

    # Segunda linha
    n = b1.winfo_y() + b1.winfo_height()

    b12 = tk.Button(
        window,
        text=choice(options[11]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window, b12, chosen_letter
        )
    )

    b12.place(x=b1.winfo_x(), y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b12)

    x = b12.winfo_x() + b12.winfo_width()

    for i in range(12, 22):
        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window, buttons[b], chosen_letter
            )
        )

        button.place(x=x, y=n, anchor="nw")
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width()

    # Terceira linha
    n = b12.winfo_y() + b12.winfo_height()

    b23 = tk.Button(
        window,
        text=choice(options[22]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window, b23, chosen_letter
        )
    )

    b23.place(x=b1.winfo_x(), y=n, anchor="nw")
    window.update_idletasks()
    buttons.append(b23)

    x = b23.winfo_x() + b23.winfo_width()

    for i in range(23, 33):
        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window, buttons[b], chosen_letter
            )
        )

        button.place(x=x, y=n, anchor="nw")
        window.update_idletasks()

        buttons.append(button)
        x += button.winfo_width()

    # Toca o áudio
    play_sound(chosen_letter)

    tempo_restante = tempo

    # Inicia o contador
    contador_id = window.after(100, atualizar_timer)

    # Troca de letra quando acabar
    timer_id = window.after(tempo, next_letter)


base = [
    ["А", "а"], ["Б", "б"], ["В", "в"], ["Г", "г"],
    ["Д", "д"], ["Е", "е"], ["Ё", "ё"], ["Ж", "ж"],
    ["З", "з"], ["И", "и"], ["Й", "й"], ["К", "к"],
    ["Л", "л"], ["М", "м"], ["Н", "н"], ["О", "о"],
    ["П", "п"], ["Р", "р"], ["С", "с"], ["Т", "т"],
    ["У", "у"], ["Ф", "ф"], ["Х", "х"], ["Ц", "ц"],
    ["Ч", "ч"], ["Ш", "ш"], ["Щ", "щ"], ["Ъ", "ъ"],
    ["Ы", "ы"], ["Ь", "ь"], ["Э", "э"], ["Ю", "ю"],
    ["Я", "я"]
]

letters = base.copy()

timer_id = None
contador_id = None
timer_label = None

tempo = 4000
tempo_restante = tempo

window = tk.Tk()
window.title("Learn Russian Alphabet")

size = 700

pos_x = (window.winfo_screenwidth() // 2) - (size // 2)
pos_y = (window.winfo_screenheight() // 2) - ((size - 200) // 2)

window.geometry(f"{size}x280+{pos_x}+{pos_y}")
window.resizable(False, False)

new_window()

# O mainloop fica somente aqui
window.mainloop()
