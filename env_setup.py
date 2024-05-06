import os
from threading import Thread
from tkinter.ttk import Progressbar, Label, Button
from tkinter import Tk, StringVar, IntVar, DISABLED, messagebox
from sys import platform

SKIP_PLATFORM_CHECK = False  # set this to True to skip the platform check

if platform != "win32" and not SKIP_PLATFORM_CHECK:
    messagebox.showerror("incompatible platform",
                         "The platform : " + platform + " may not run correctly Blanko's calculator.\n\n" +
                         "Set SKIP_PLATFORM_CHECK to True to skip this.")
    exit(1)

modules = (
    "customtkinter",
    "pillow"
)
modules_count = len(modules)
i = 0

cancel = False
stopped = False


def cancel_cmd():
    global stopped
    global cancel

    cancel = True
    progress_label_var.set("canceling...")
    cancel_button["state"] = DISABLED
    while not stopped:
        root.update()

    root.destroy()


def install_thread():
    global i
    global stopped

    for module in modules:
        if cancel:
            stopped = True
            break
        progress_label_var.set("installing : " + module)
        os.system("pip install " + module)
        i += 1
        progress_var.set(round((i/modules_count)*100))
    stopped = True
    cancel_button["state"] = DISABLED
    progress_label_var.set("finish")
    root.after(500, root.destroy)



install_thread_object = Thread(target=install_thread)

root = Tk()

root.resizable(False, False)
root.title("env setup")

root.protocol("WM_DELETE_WINDOW", cancel_cmd)

progress_label_var = StringVar(root, "initialising...")
progress_label = Label(root, textvariable=progress_label_var, justify="left")
progress_label.pack(fill="x", padx=35, pady=(30, 0))

progress_var = IntVar(root, 0)
progress_bar = Progressbar(root, variable=progress_var, length=300)
progress_bar.pack(expand=True, padx=30, pady=(0, 20))

cancel_button = Button(root, text="cancel", command=cancel_cmd)
cancel_button.pack(pady=(0, 20))

install_thread_object.start()

root.mainloop()
