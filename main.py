from tkinter import StringVar
from customtkinter import CTk, CTkLabel, CTkFrame, CTkButton, set_appearance_mode
from time import time
set_appearance_mode("system")


def close():
    global run
    run = False


def update():
    global cursor_x
    global cursor_y
    global window_x
    global window_y
    global window_width
    global window_height
    global x_check
    global y_check

    cursor_x = root.winfo_pointerx()
    cursor_y = root.winfo_pointery()

    window_x = root.winfo_x()
    window_y = root.winfo_y()

    window_width = root.winfo_width()
    window_height = root.winfo_height()

    x_check = cursor_x > window_x and cursor_x < window_x + window_width
    y_check = cursor_y > window_y and cursor_y < window_y + window_height


def buttons_cmd(button_id: str):
    global calcul

    if button_id == "=":
        try:
            calcul = str(eval(calcul))
            if len(calcul) >= 36:
                calcul = "error : the result is too big"
        except ZeroDivisionError:
            calcul = "error : Division by Zero"
        except:calcul = "error"

    elif button_id == "C":
        result_label.configure(font=("sans-serif", 30))
        calcul = "0"
    elif button_id == "CE":
        if calcul[:5] == "error":
            result_label.configure(font=("sans-serif", 30))
            calcul = "0"
        else:
            return
    elif calcul[:5] == "error":
        return
    elif len(calcul) >= 36:
        return
    elif button_id == "<-":
        if len(calcul) <= 1:
            calcul = "0"
        else:
            calcul = calcul[:-1]
    else:
        if calcul == "0":
            calcul = button_id
        else:
            if button_id == "x":
                calcul = calcul + "*"
            else:
                calcul = calcul + button_id

    if len(calcul) >= 32:
        pass
    elif len(calcul) > 12:
        result_label.configure(font=("sans-serif", round(30-(len(calcul)/1.6))))
    result_var.set(calcul)


font = ("sans-serif", 30)

root = CTk()

root.attributes("-alpha", 0.98)
root.attributes("-topmost", True)

root.geometry("250x390+30+30")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", close)

root.title("Calculator")
root.iconbitmap("calculator.ico")


def focus_in(event):
    global focus
    print("focus in :", event)
    focus = True


def focus_out(event):
    global focus
    print("focus out :", event)
    focus = False


focus = True
root.bind("<FocusIn>", focus_in)
root.bind("<FocusOut>", focus_out)

result_frame = CTkFrame(root, height=60)
result_frame.pack(fill="x", side="top", padx=10, pady=10)
result_frame.propagate(False)

result_var = StringVar(result_frame, "0")
result_label = CTkLabel(result_frame, textvariable=result_var, font=font)
result_label.pack(side="right", padx=(0, 10))

buttons_frame = CTkFrame(root)
buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
buttons_frame.propagate(False)

buttons = [
    [["C"], ["CE"], None, ["<-"]],
    [["1"], ["2"], ["3"], ["/"]],
    [["4"], ["5"], ["6"], ["x"]],
    [["7"], ["8"], ["9"], ["-"]],
    [["."], ["0"], ["="], ["+"]]
]
special_color = ["+", "-", "x", "/", "<-", "."]

row = 0
for line in buttons:
    column = 0
    root.grid_columnconfigure(column, weight=1, uniform="same_group")
    for button in line:
        if button is not None:
            root.grid_rowconfigure(row, weight=0)
            if button[0] in special_color:
                color = {"fg_color": ("#1f6aa2", "#16537e"), "hover_color": "#16486b"}
            elif button[0] == "C" or button[0] == "CE":
                color = {"fg_color": ("#cc5555", "#cc0000"), "hover_color": ("#995555","#990000")}
            elif button[0] == "=":
                color = {"fg_color": ("#5b5b5b", "#3b3b3b"), "hover_color": ("#7b7b7b", "#5b5b5b")}
            else:
                color = {"fg_color": None}

            tmp = CTkButton(buttons_frame, text=button[0], width=53.5, height=53.5, font=("sans-serif", 20), **color, command=lambda button_id=button[0]: buttons_cmd(button_id))
            tmp.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            button.append(tmp)
        column += 1
    row += 1

calcul = ""

last_time = 0

run = True
while run:
    last_time = time()
    update()

    while x_check and y_check:
        if focus:
            break
        if (time() - last_time) >= 0.4:
            current = root.attributes("-alpha")
            if current != 0:
                root.attributes("-alpha", current - 0.0003)
        root.update()

        update()

    if focus:
        root.attributes("-alpha", 0.98)
    else:
        root.attributes("-alpha", 0.7)

    root.update()
root.destroy()
