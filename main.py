from ctypes import windll
from threading import Thread
from tkinter import StringVar, messagebox
from customtkinter import CTkLabel, CTkFrame, CTkButton, CTkOptionMenu, CTkImage, set_appearance_mode
from time import time
from PIL import Image
from os import system, path, remove
from platform import python_version
from webbrowser import open as openlink
from tkinterdnd2 import DND_ALL
from json import loads

from libs.config import CalculatorConfig
from libs.widgets import Window, FloatSpinbox
import libs.translation as translation

LETTERS = "abcdefghijklmnopqrstuvwxyz"
set_to_foreground = windll.user32.SetForegroundWindow
language = translation.Language()

config = CalculatorConfig()

language.set_language(config.LANG.get_id())
delta_time = 0
last_time = time()
last_dt = 0

VERSION = "1.1"
PYTHON_VERSION = python_version()
CREDIS = [f"{language.DEVELOPER} : Blanko83", f"{language.ABOUT_ICON} : https://www.flaticon.com/", f"{language.SETTINGS_ICON} : https://www.flaticon.com/", f"{language.BACK_ICON} : https://www.flaticon.com/"]

tmp = ""
for credit in CREDIS:
    tmp = tmp + credit + '\n'


CREDIS = tmp
set_appearance_mode(config.THEME.get())


def check_security(data):
    for c in LETTERS:
        if c in data:
            return False
    return True

def invert_dict(obj : dict):
    tmp = {}
    keys = obj.keys().__iter__()
    for value in obj.values():
        tmp[value] = keys.__next__()
    
    return tmp

def close():
    global run
    run = False


def focus_in(event):
    global focus
    print("focus in :", event)
    focus = True


def focus_out(event):
    global focus
    print("focus out :", event)
    focus = False


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
        if not check_security(calcul):
            calcul = "error"
        try:
            calcul = str(eval(calcul))
            if len(calcul) >= 36:
                calcul = "error : the result is too big"
        except ZeroDivisionError:
            calcul = "error : Division by Zero"
        except:
            calcul = "error"

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


def open_settings():
    main_frame.place_forget()
    settings_frame.place(**FRAMES_PLACE_ARGS)


def close_settings():
    main_frame.place(**FRAMES_PLACE_ARGS)
    settings_frame.place_forget()


def open_info():
    main_frame.place_forget()
    info_frame.place(**FRAMES_PLACE_ARGS)


def close_info():
    main_frame.place(**FRAMES_PLACE_ARGS)
    info_frame.place_forget()


def update_lang(value):
    global run
    config.LANG.set(value)
    config.LANG.validate()
    run = False
    tmp_thread = Thread(target = system, args=[__file__])
    tmp_thread.start()


def update_theme(value):
    translated_value = language.THEME_MENU_VALUE[value]
    set_appearance_mode(translated_value)
    config.THEME.set(translated_value)
    config.THEME.validate()


def update_hide_delay():
    config.HIDE_DELAY.set(hide_delay_spin_box.get())
    config.HIDE_DELAY.validate()


def drop_cmd(event):
    global calcul
    global language
    data = event.data.split(" ")
    for paths in data:
        if path.exists(paths) and paths.split(".")[-1] == "bcl":
            file_r = open(paths, "r")
            tmp = file_r.read()
            tmp_json = loads(tmp)
            if not translation.check_validity(tmp_json):
                messagebox.showerror("invalid file", "this file is invalid")
            else:
                file = open(f"lang/{path.basename(paths)}", "w")
                file.write(tmp)
                file.close()
                file_r.close()
                update_lang(tmp_json["alias"])


        else:
            calcul = paths
            buttons_cmd("=")
            break


def drop_start(event):
    set_to_foreground(root.winfo_id())


font = ("sans-serif", 30)

root = Window()

root.attributes("-alpha", 0.98)
root.attributes("-topmost", True)

root.geometry("250x420+30+30")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", close)

root.title(language.TITLE)
root.iconbitmap("src/calculator.ico")

root.dnd_bind('<<Drop>>', drop_cmd)
root.dnd_bind("<<DropEnter>>", drop_start)
root.drop_target_register(DND_ALL)

root.bind("<FocusIn>", focus_in)
root.bind("<FocusOut>", focus_out)

default_secondary_button_config = {"text": "", "fg_color": root._fg_color, "hover_color": ("#5b5b5b", "#3b3b3b"), "width": 30, "height": 30, "cursor": "arrow"}


FRAMES_PLACE_ARGS = {"x": 0, "y": 0, "relwidth": 1, "relheight": 1}
main_frame = CTkFrame(root, fg_color=root._fg_color, corner_radius=0)
main_frame.place(**FRAMES_PLACE_ARGS)

settings_frame = CTkFrame(root, fg_color=root._fg_color, corner_radius=0)

settings_top_frame = CTkFrame(settings_frame, fg_color=root._fg_color, height=20)
settings_top_frame.pack(fill="x", side="top")

back_from_info_image_dark_file = Image.open("src/ui_icons/dark/back.png")
back_from_info_image_light_file = Image.open("src/ui_icons/light/back.png")
back_from_info_image = CTkImage(back_from_info_image_light_file, back_from_info_image_dark_file, (15, 15))
back_from_info_button = CTkButton(settings_top_frame, image=back_from_info_image, **default_secondary_button_config, command=close_settings)
back_from_info_button.propagate(False)
back_from_info_button.pack(side="left", padx=5, pady=5)

info_box = CTkFrame(settings_frame)
info_box.pack(expand=True, fill="both", padx=5, pady=5)

h2_options = {"font": ("sans-serif", 20), "justify": "left"}
info_options = {"justify": "center"}
menu_options = {"font": ("sans-serif", 15), "dropdown_font": ("sans-serif", 15)}

info_title = CTkLabel(settings_top_frame, text=language.SETTINGS_TITLE, justify="left", font=("sans-serif", 20))
info_title.pack(side="left", padx=20, pady=(5, 0))

lang_label = CTkLabel(info_box, text=language.LANGUAGE_OPTION_TEXT, **h2_options)
lang_label.propagate(False)
lang_label.pack(fill="x", pady=(25, 0))

lang_info = CTkLabel(info_box, text=language.LANGUAGE_INFO, **info_options)
lang_info.propagate(False)
lang_info.pack(fill="x")

lang_menu = CTkOptionMenu(info_box, values=language.languages_alias, **menu_options, command=update_lang)
lang_menu.pack(fill="x", padx=5, pady=10)
lang_menu.set(config.LANG.get())

theme_label = CTkLabel(info_box, text=language.THEME_OPTION_TEXT, **h2_options)
theme_label.propagate(False)
theme_label.pack(fill="x")

theme_info = CTkLabel(info_box, text=language.THEME_INFO, **info_options)
theme_info.propagate(False)
theme_info.pack(fill="x")

theme_menu = CTkOptionMenu(info_box, values=list(language.THEME_MENU_VALUE.keys()), **menu_options, command=update_theme)
theme_menu.pack(fill="x", padx=5, pady=10)
theme_menu.set(invert_dict(language.THEME_MENU_VALUE)[(config.THEME.get())])

hide_delay_label = CTkLabel(info_box, text=language.HIDE_DELAY_OPTION_TEXT, **h2_options)
hide_delay_label.pack(fill="x")
hide_delay_label.propagate(False)

hide_delay_info = CTkLabel(info_box, text=language.HIDE_DELAY_INFO, **info_options)
hide_delay_info.propagate(False)
hide_delay_info.pack(fill="x")

hide_delay_spin_box = FloatSpinbox(info_box, step_size=0.1,_from=0.1,  to=10, value=0.2, command=update_hide_delay)
hide_delay_spin_box.pack(fill="x", padx=40, pady=10)
hide_delay_spin_box.set(config.HIDE_DELAY.get())

top_frame = CTkFrame(main_frame, fg_color=root._fg_color, height=20)
top_frame.pack(fill="x")

title_label = CTkLabel(top_frame, text=language.TITLE, justify="left", font=("sans-serif", 20))
title_label.pack(side="left", padx=20, pady=(5, 0))


settings_image_dark_file = Image.open("src/ui_icons/dark/settings.png")
settings_image_light_file = Image.open("src/ui_icons/light/settings.png")
settings_image = CTkImage(settings_image_light_file, settings_image_dark_file, (15, 15))
settings_button = CTkButton(top_frame, image=settings_image, **default_secondary_button_config, command=open_settings)
settings_button.propagate(False)
settings_button.pack(side="right", padx=0, pady=5)

info_image_dark_file = Image.open("src/ui_icons/dark/info.png")
info_image_light_file = Image.open("src/ui_icons/light/info.png")
info_image = CTkImage(info_image_light_file, info_image_dark_file, (15, 15))
info_button = CTkButton(top_frame, image=info_image, **default_secondary_button_config, command=open_info)
info_button.propagate(False)
info_button.pack(side="right", padx=0, pady=5)


info_frame = CTkFrame(root, fg_color=root._fg_color, corner_radius=0)

info_top_frame = CTkFrame(info_frame, fg_color=root._fg_color, height=20)
info_top_frame.pack(fill="x", side="top")

back_from_info_image_dark_file = Image.open("src/ui_icons/dark/back.png").transpose(Image.FLIP_LEFT_RIGHT)
back_from_info_image_light_file = Image.open("src/ui_icons/light/back.png").transpose(Image.FLIP_LEFT_RIGHT)
back_from_info_image = CTkImage(back_from_info_image_light_file, back_from_info_image_dark_file, (15, 15))
# close_info
back_from_info_button = CTkButton(info_top_frame, image=back_from_info_image, **default_secondary_button_config, command=close_info)
back_from_info_button.propagate(False)
back_from_info_button.pack(side="right", padx=5, pady=5)

info_box = CTkFrame(info_frame)
info_box.pack(expand=True, fill="both", padx=5, pady=5)

info_title = CTkLabel(info_top_frame, text=language.ABOUT, justify="left", font=("sans-serif", 20))
info_title.pack(side="left", padx=20, pady=(5, 0))

version_label_title = CTkLabel(info_box, text=language.VERSION, font=("sans-serif", 20))
version_label_title.pack()

version_label_var = StringVar(info_box, f"{language.PYTHON_VERSION} : {PYTHON_VERSION}\n{language.APP_VERSION} : {VERSION}")
version_label = CTkLabel(info_box, textvariable=version_label_var)
version_label.pack(pady=(0, 10))


credis_label_title = CTkLabel(info_box, text=language.CREDITS, font=("sans-serif", 20))
credis_label_title.pack()

python_version_label = CTkLabel(info_box, text=CREDIS)
python_version_label.pack()

release_label_title = CTkLabel(info_box, text=language.RELEASE_NOTE, font=("sans-serif", 20))
release_label_title.pack()

release_button_link = CTkButton(info_box, text=language.GO_TO_GITHUB, command=lambda: openlink("https://github.com/BlankoDev/Blanko-s-calculator/releases"))
release_button_link.pack(pady=20)

result_frame = CTkFrame(main_frame, height=60)
result_frame.pack(fill="x", side="top", padx=10, pady=5)
result_frame.propagate(False)

result_var = StringVar(result_frame, "0")
result_label = CTkLabel(result_frame, textvariable=result_var, font=font)
result_label.pack(side="right", padx=(0, 10))

buttons_frame = CTkFrame(main_frame)
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
focus = True
last_time = 0

run = True
while run:
    last_time = time()
    update()

    while x_check and y_check:
        if focus:
            break
        if (time() - last_time) >= config.HIDE_DELAY.get():
            current = root.attributes("-alpha")
            if current != 0:
                root.attributes("-alpha", current - 0.0003)
        update()
        root.update()

    if focus:
        root.attributes("-alpha", 0.98)
    else:
        root.attributes("-alpha", 0.7)

    root.update()

root.destroy()
config.close()