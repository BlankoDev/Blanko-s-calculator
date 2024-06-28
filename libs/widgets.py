from typing import Union, Callable
from customtkinter import CTk, CTkButton, CTkFrame, CTkEntry
from tkinterdnd2.TkinterDnD import DnDWrapper, _require


class Window(CTk, DnDWrapper):
    def __init__(self, *args, **kw):
        CTk.__init__(self, *args, **kw)
        self.TkdndVersion = _require(self)


class FloatSpinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 value : float = 0,
                 step_size: Union[int, float] = 1,
                 _from : float = 0,
                 to : float = 10,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self._from = _from
        self.to = to

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)


        self.entry.insert(0, str(value))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            val_add = float(self.entry.get())
            value = round(val_add + self.step_size, 1)
            if not (value >= self.to):
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            val_sub = float(self.entry.get())
            value = round(val_sub - self.step_size, 1)
            if not (value <= self._from):
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        if (not (value >= self.to)) or (not (value <= self._from)):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(float(value)))