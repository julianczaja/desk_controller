import tkinter as tk
import time
from ctypes import windll

DIALOG_TIMEOUT = 2000
FONT_SIZE = 14
DIALOG_WIDTH = 400
DIALOG_HEIGHT = 100
BACKGROUND_COLOR = "#f0f0f0"

ICONS_DIR_PATH = "~/Desktop/desk_controller/icons"

class GuiController:

    def __init__(self):

        windll.shcore.SetProcessDpiAwareness(1)  # to fix blurr problems

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

        self.win.geometry("{}x{}".format(DIALOG_WIDTH, DIALOG_HEIGHT))
        self.win.geometry("+{}+{}".format(ws-DIALOG_WIDTH-10, hs-DIALOG_HEIGHT-55))

        self.frame = tk.Frame(self.win,bg=BACKGROUND_COLOR, highlightbackground="black", highlightthickness=4)
        self.frame.pack(expand=True, fill=tk.BOTH)

        font = ("Roboto Light", FONT_SIZE)
        self.dialog_label = tk.Label(self.frame, font=font, bg=BACKGROUND_COLOR)
        self.dialog_label.place(relx=0.5, rely=0.5, anchor="center")

        self.volume_image = tk.PhotoImage(file="{}/volume.png".format(ICONS_DIR_PATH))
        self.volume_image = self.__switchColors(self.volume_image, "#ffffff", BACKGROUND_COLOR)
        self.volume_i = tk.Label(self.frame, image=self.volume_image, borderwidth=0)

        self.brightness_image = tk.PhotoImage(file="{}/brightness.png".format(ICONS_DIR_PATH))
        self.brightness_image = self.__switchColors(self.brightness_image, "#ffffff", BACKGROUND_COLOR)
        self.brightness_i = tk.Label(self.frame, image=self.brightness_image, borderwidth=0)

        self.is_dialog_created = True

    def update(self):
        t_now = time.time() * 1000
        d_time = t_now - self.last_dialog_shown

        if self.is_dialog_shown and d_time > DIALOG_TIMEOUT:
            self.win.withdraw()
            self.is_dialog_shown = False

        self.win.update()

    def hide(self):
        self.win.withdraw()

    def show(self):
        self.win.deiconify()

    def show_volume_message(self, msg):
        self.__show_message(msg)
        self.__hide_brightness_icon()
        self.__show_volume_icon()

    def show_brightness_message(self, msg):
        self.__show_message(msg)
        self.__show_brightness_icon()
        self.__hide_volume_icon()

    def show_general_message(self, msg):
        self.__show_message(msg)
        self.__hide_brightness_icon()
        self.__hide_volume_icon()

    def __show_message(self, msg):
        if not self.is_dialog_created:
            self.create_dialog()

        self.show()
        self.dialog_label.configure(text=msg)
        self.is_dialog_shown = True
        self.last_dialog_shown = time.time() * 1000

    def __show_brightness_icon(self):
        self.brightness_i.place(relx=0.15, rely=0.5, anchor="center")
        
    def __hide_brightness_icon(self):
        self.brightness_i.place_forget()

    def __show_volume_icon(self):
        self.volume_i.place(relx=0.15, rely=0.5, anchor="center")
        
    def __hide_volume_icon(self):
        self.volume_i.place_forget()

    def __switchColors(self, img, currentColor, futureColor):
        newPhotoImage = tk.PhotoImage(width=img.width(), height=img.height())
        for x in range(img.width()):
            for y in range(img.height()):
                rgb = '#%02x%02x%02x' % img.get(x, y)
                if rgb == currentColor:
                    newPhotoImage.put(futureColor, (x, y))
                else:
                    newPhotoImage.put(rgb, (x, y))
        return newPhotoImage

if __name__ == "__main__":
    gui_controller = GuiController()

    t = time.time()
    gui_controller.show_general_message("Test message")
    while (time.time() - t) < 1:
        gui_controller.update()
        time.sleep(0.1)

    t = time.time()
    gui_controller.show_volume_message(" Volume: 20.5")
    while (time.time() - t) < 1:
        gui_controller.update()
        time.sleep(0.1)

    t = time.time()
    gui_controller.show_brightness_message("  Brightness: 50.5")
    while (time.time() - t) < 1:
        gui_controller.update()
        time.sleep(0.1)
