import tkinter as tk
import time
from ctypes import windll

DIALOG_TIMEOUT = 2000
FONT_SIZE = 14


class GuiController:

    def __init__(self):
        
        windll.shcore.SetProcessDpiAwareness(1) # to fix blurr problems

        self.win = tk.Tk()
        self.hide()

        self.is_dialog_created = False
        self.is_dialog_shown = False
        self.dialog_label = None
        self.last_dialog_shown = 0

    def create_dialog(self):
        print("Creating dialog")

        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.resizable(False, False)

        ws = self.win.winfo_screenwidth()
        hs = self.win.winfo_screenheight()

        self.win.geometry("300x100")
        self.win.geometry("+{}+{}".format(ws-310, hs-155))

        font = ("Roboto Light", FONT_SIZE)
        self.dialog_label = tk.Label(text="null", font=font)
        self.dialog_label.grid(row=0, column=0)
        self.dialog_label.pack(expand=True)
        

        self.is_dialog_created = True

    def update(self):
        t_now = time.time() * 1000
        d_time = t_now - self.last_dialog_shown

        if self.is_dialog_shown and d_time > DIALOG_TIMEOUT:
            self.win.withdraw()
            self.is_dialog_shown = False

        self.win.update()

    def show_message(self, msg):
        if not self.is_dialog_created:
            self.create_dialog()

        self.show()
        self.dialog_label.configure(text=msg)
        self.is_dialog_shown = True
        self.last_dialog_shown = time.time() * 1000

    def hide(self):
        self.win.withdraw()

    def show(self):
        self.win.deiconify()
