import tkinter as tk
from pygame import mixer
from random import choice, shuffle, randint
import time


# =========================================================
# ÁUDIO
# =========================================================

def play_sound(letra):
    mixer.init()

    # Para o áudio anterior
    mixer.music.stop()

    v = randint(0, 3)

    arquivo = f"audios/{letra[0]}{letra[1]}({v}).mp3"

    mixer.music.load(arquivo)
    mixer.music.play()


# =========================================================
# RESETAR BOTÃO
# =========================================================

def reset_button(button):
    global reset_id

    # Só tenta alterar se o botão ainda existir
    if button.winfo_exists():
        button.config(bg="SystemButtonFace")

    reset_id = None


# =========================================================
# IR PARA A PRÓXIMA LETRA
# =========================================================

def next_letter():
    global timer_id
    global contador_id
    global reset_id

    # Cancela o timer principal
    if timer_id is not None:
        try:
            window.after_cancel(timer_id)
        except tk.TclError:
            pass

        timer_id = None

    # Cancela o contador visual
    if contador_id is not None:
        try:
            window.after_cancel(contador_id)
        except tk.TclError:
            pass

        contador_id = None

    # Cancela o reset de botão errado
    if reset_id is not None:
        try:
            window.after_cancel(reset_id)
        except tk.TclError:
            pass

        reset_id = None

    # Remove todos os widgets da rodada anterior
    for widget in window.winfo_children():
        widget.destroy()

    # Cria a próxima rodada
    new_window()


# =========================================================
# VERIFICAR RESPOSTA
# =========================================================

def check_answer(wind, button, correct_letter):
    global timer_id
    global contador_id
    global reset_id

    # Se o botão já não existir, não faz nada
    if not button.winfo_exists():
        return

    # -----------------------------------------------------
    # RESPOSTA CORRETA
    # -----------------------------------------------------

    if button.cget("text") in correct_letter:

        button.config(bg="green")

        # Para o timer principal
        if timer_id is not None:
            try:
                wind.after_cancel(timer_id)
            except tk.TclError:
                pass

            timer_id = None

        # Para o contador visual
        if contador_id is not None:
            try:
                wind.after_cancel(contador_id)
            except tk.TclError:
                pass

            contador_id = None

        # Cancela eventual reset de botão
        if reset_id is not None:
            try:
                wind.after_cancel(reset_id)
            except tk.TclError:
                pass

            reset_id = None

        # Espera meio segundo antes da próxima letra
        wind.after(500, next_letter)

    # -----------------------------------------------------
    # RESPOSTA ERRADA
    # -----------------------------------------------------

    else:

        button.config(bg="red")

        # Se já havia um reset agendado, cancela
        if reset_id is not None:
            try:
                wind.after_cancel(reset_id)
            except tk.TclError:
                pass

            reset_id = None

        # Volta a cor do botão depois de 500 ms
        reset_id = wind.after(
            500,
            lambda: reset_button(button)
        )


# =========================================================
# ATUALIZAR CONTADOR
# =========================================================

def atualizar_timer():
    global contador_id
    global timer_label
    global tempo_inicio

    # Verifica quanto tempo realmente passou
    decorrido = (time.perf_counter() - tempo_inicio) * 1000

    restante = tempo - decorrido

    # -----------------------------------------------------
    # TEMPO ESGOTADO
    # -----------------------------------------------------

    if restante <= 0:

        if timer_label is not None and timer_label.winfo_exists():
            timer_label.config(text="0.0")

        contador_id = None
        return

    # -----------------------------------------------------
    # ATUALIZA TEXTO
    # -----------------------------------------------------

    segundos = restante / 1000

    if timer_label is not None and timer_label.winfo_exists():
        timer_label.config(text=f"{segundos:.1f}")

    # Continua atualizando
    contador_id = window.after(
        50,
        atualizar_timer
    )


# =========================================================
# CRIAR NOVA RODADA
# =========================================================

def new_window():
    global letters
    global window
    global size
    global timer_id
    global contador_id
    global tempo_inicio
    global timer_label

    # -----------------------------------------------------
    # REINICIA A LISTA QUANDO TODAS AS LETRAS FOREM USADAS
    # -----------------------------------------------------

    if len(letters) == 0:
        letters = base.copy()

    # Escolhe uma letra
    chosen_letter = choice(letters)

    # Remove para não repetir até acabar a lista
    letters.remove(chosen_letter)

    # -----------------------------------------------------
    # CRIA AS OPÇÕES
    # -----------------------------------------------------

    options = base.copy()
    shuffle(options)

    button_font = 22
    button_height = 1
    button_width = 3

    # -----------------------------------------------------
    # BOTÃO DE REPETIR ÁUDIO
    # -----------------------------------------------------

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

    n = (
        playsoundagin.winfo_y()
        + playsoundagin.winfo_height()
        + 25
    )

    # -----------------------------------------------------
    # CONTADOR
    # -----------------------------------------------------

    timer_label = tk.Label(
        window,
        text=f"{tempo / 1000:.1f}",
        font=("Arial", 20)
    )

    timer_label.place(
        x=size - 30,
        y=25,
        anchor="ne"
    )

    # =====================================================
    # BOTÕES
    # =====================================================

    buttons = []

    # -----------------------------------------------------
    # PRIMEIRA LINHA
    # -----------------------------------------------------

    b1 = tk.Button(
        window,
        text=choice(options[0]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window,
            b1,
            chosen_letter
        )
    )

    b1.place(
        x=14,
        y=n,
        anchor="nw"
    )

    window.update_idletasks()

    buttons.append(b1)

    x = (
        b1.winfo_x()
        + b1.winfo_width()
    )

    for i in range(1, 11):

        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window,
                buttons[b],
                chosen_letter
            )
        )

        button.place(
            x=x,
            y=n,
            anchor="nw"
        )

        window.update_idletasks()

        buttons.append(button)

        x += button.winfo_width()

    # -----------------------------------------------------
    # SEGUNDA LINHA
    # -----------------------------------------------------

    n = (
        b1.winfo_y()
        + b1.winfo_height()
    )

    b12 = tk.Button(
        window,
        text=choice(options[11]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window,
            b12,
            chosen_letter
        )
    )

    b12.place(
        x=b1.winfo_x(),
        y=n,
        anchor="nw"
    )

    window.update_idletasks()

    buttons.append(b12)

    x = (
        b12.winfo_x()
        + b12.winfo_width()
    )

    for i in range(12, 22):

        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window,
                buttons[b],
                chosen_letter
            )
        )

        button.place(
            x=x,
            y=n,
            anchor="nw"
        )

        window.update_idletasks()

        buttons.append(button)

        x += button.winfo_width()

    # -----------------------------------------------------
    # TERCEIRA LINHA
    # -----------------------------------------------------

    n = (
        b12.winfo_y()
        + b12.winfo_height()
    )

    b23 = tk.Button(
        window,
        text=choice(options[22]),
        font=("Arial", button_font),
        width=button_width,
        height=button_height,
        command=lambda: check_answer(
            window,
            b23,
            chosen_letter
        )
    )

    b23.place(
        x=b1.winfo_x(),
        y=n,
        anchor="nw"
    )

    window.update_idletasks()

    buttons.append(b23)

    x = (
        b23.winfo_x()
        + b23.winfo_width()
    )

    for i in range(23, 33):

        button = tk.Button(
            window,
            text=choice(options[i]),
            font=("Arial", button_font),
            width=button_width,
            height=button_height,
            command=lambda b=i: check_answer(
                window,
                buttons[b],
                chosen_letter
            )
        )

        button.place(
            x=x,
            y=n,
            anchor="nw"
        )

        window.update_idletasks()

        buttons.append(button)

        x += button.winfo_width()

    # =====================================================
    # COMEÇA A RODADA
    # =====================================================

    # Toca o áudio da letra
    play_sound(chosen_letter)

    # Marca o momento exato em que começou
    tempo_inicio = time.perf_counter()

    # Inicia o contador visual
    contador_id = window.after(
        50,
        atualizar_timer
    )

    # Agenda a troca da letra
    timer_id = window.after(
        tempo,
        next_letter
    )


# =========================================================
# ALFABETO RUSSO
# =========================================================

base = [
    ["А", "а"],
    ["Б", "б"],
    ["В", "в"],
    ["Г", "г"],
    ["Д", "д"],
    ["Е", "е"],
    ["Ё", "ё"],
    ["Ж", "ж"],
    ["З", "з"],
    ["И", "и"],
    ["Й", "й"],
    ["К", "к"],
    ["Л", "л"],
    ["М", "м"],
    ["Н", "н"],
    ["О", "о"],
    ["П", "п"],
    ["Р", "р"],
    ["С", "с"],
    ["Т", "т"],
    ["У", "у"],
    ["Ф", "ф"],
    ["Х", "х"],
    ["Ц", "ц"],
    ["Ч", "ч"],
    ["Ш", "ш"],
    ["Щ", "щ"],
    ["Ъ", "ъ"],
    ["Ы", "ы"],
    ["Ь", "ь"],
    ["Э", "э"],
    ["Ю", "ю"],
    ["Я", "я"]
]


# =========================================================
# VARIÁVEIS
# =========================================================

letters = base.copy()

timer_id = None
contador_id = None
reset_id = None

timer_label = None

# Tempo de cada rodada em milissegundos
tempo = 5000

# Momento em que o contador começou
tempo_inicio = 0


# =========================================================
# JANELA
# =========================================================

window = tk.Tk()

window.title("Learn Russian Alphabet")

size = 700

pos_x = (
    window.winfo_screenwidth() // 2
    - size // 2
)

pos_y = (
    window.winfo_screenheight() // 2
    - (size - 200) // 2
)

window.geometry(
    f"{size}x280+{pos_x}+{pos_y}"
)

window.resizable(False, False)


# =========================================================
# PRIMEIRA RODADA
# =========================================================

new_window()


# =========================================================
# LOOP PRINCIPAL
# =========================================================

window.mainloop()
