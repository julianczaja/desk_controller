import tkinter as tk
import time
from ctypes import windll
from infi.systray import SysTrayIcon

DIALOG_TIMEOUT = 2000
FONT_SIZE = 10
DIALOG_WIDTH = 290
DIALOG_HEIGHT = 75
BACKGROUND_COLOR = "#2e2e2e"
TRANSPARENT_COLOR = "#00ff00"

ICONS_DIR_PATH = "~/Desktop/desk_controller/icons"

class RoundedProgressBar(tk.Canvas):
    def __init__(
        self,
        parent,
        width,
        height,
        bg_color,
        fg_color,
        outline_color,
        corner_radius,
        max_value=100,
        *args,
        **kwargs
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
            *args,
            **kwargs
        )
        self.configure(bg=TRANSPARENT_COLOR)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.outline_color = outline_color
        self.corner_radius = corner_radius
        self.max_value = max_value
        self.value = 0
        self._draw_rounded_bar()

    def _draw_rounded_bar(self):
        self.delete("all")

        # Draw background with rounded corners
        self.create_round_rect(
            0,
            0,
            self.width,
            self.height,
            self.corner_radius,
            fill=self.bg_color,
            outline=self.outline_color,
        )

        # Draw foreground (progress) with rounded corners
        fill_width = (self.value / self.max_value) * self.width
        if fill_width > 0:
            self.create_round_rect(
                0,
                0,
                fill_width,
                self.height,
                self.corner_radius,
                fill=self.fg_color,
                outline=self.outline_color,
            )

    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def set_value(self, value):
        self.value = value
        self._draw_rounded_bar()

class GuiController:

    def __init__(self, exit_callback):
        windll.shcore.SetProcessDpiAwareness(1)  # to fix blurr problems

        self.win = tk.Tk()
        self.exit_callback = exit_callback
        self.create_tray_icon()
        self.is_dialog_created = False
        self.is_dialog_shown = False
        self.dialog_label = None
        self.last_dialog_shown = 0

    def create_dialog(self):
        print("Creating dialog")

        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.win.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.win.resizable(False, False)

        ws = self.win.winfo_screenwidth()
        hs = self.win.winfo_screenheight()

        self.target_x = int(ws/2)-int(DIALOG_WIDTH/2)
        self.target_y = hs-DIALOG_HEIGHT-20

        self.win.geometry("{}x{}".format(DIALOG_WIDTH, DIALOG_HEIGHT))
        self.win.geometry("+{}+{}".format(self.target_x, self.target_y))

        self.frame = RoundedProgressBar(
            self.win,
            width=DIALOG_WIDTH,
            height=DIALOG_HEIGHT,
            bg_color=BACKGROUND_COLOR,
            fg_color=BACKGROUND_COLOR,
            outline_color="#000000",
            corner_radius=20,
        )
        self.frame.pack(expand=True, fill=tk.BOTH)

        font = ("Roboto Light", FONT_SIZE)
        self.dialog_label = tk.Label(self.frame, font=font, bg=BACKGROUND_COLOR,fg="#ffffff")
        self.dialog_label.place(relx=0.5, rely=0.5, anchor="center")

        value_font = ("Roboto Light", 10)
        self.dialog_value_label = tk.Label(self.frame, font=value_font, 
                                           bg=BACKGROUND_COLOR, fg="#ffffff")
        self.dialog_value_label.place(relx=0.90, rely=0.5, anchor="center")

        self.brightness_image = tk.PhotoImage(  file="{}/brightness.png".format(ICONS_DIR_PATH))
        self.brightness_i = tk.Label(self.frame, image=self.brightness_image, borderwidth=0)

        self.brightness_progress = RoundedProgressBar(
            self.frame,
            width=160,
            height=6,
            bg_color="#9f9f9f",
            fg_color="#4cc2ff",
            outline_color="#9f9f9f",
            corner_radius=10,
        )
        self.brightness_progress.place(relx=0.5, rely=0.5, anchor="center")

        self.is_dialog_created = True

    def update(self):
        t_now = time.time() * 1000
        d_time = t_now - self.last_dialog_shown

        if self.is_dialog_shown and d_time > DIALOG_TIMEOUT:
            self.hide()
            self.is_dialog_shown = False

        self.win.update_idletasks()
        self.win.update()

    def create_tray_icon(self):
        print("create_tray_icon")
        tray_menu = ()
        self.systray = SysTrayIcon(
            icon = "dial_knob.ico",
            hover_text = "Example tray icon",
            menu_options = tray_menu,
            on_quit = self.on_quit_callback,
        )
        self.systray.start()

    def hide(self):
        print("hide")
        self.win.withdraw()

    def show(self):
        print("show")
        self.win.deiconify()

    def quit_window(self):
        print("quit_window")
        self.systray.shutdown()

    def on_quit_callback(self, systray):
        self.exit_callback()

    def show_brightness(self, value):
        self.brightness_progress.set_value(value)
        self.__hide_message()
        self.__show_value(value)
        self.__show_brightness_icon()
        self.__show_brightness_progressbar()

    def show_general_message(self, msg):
        self.__show_message(msg)
        self.__hide_brightness_icon()
        self.__hide_brightness_progressbar()

    def exit(self):
        self.win.withdraw()
        self.systray.shutdown()

    def __show_message(self, msg):
        if not self.is_dialog_created:
            self.create_dialog()
        
        self.show()
        self.dialog_label.configure(text=msg)
        self.is_dialog_shown = True
        self.last_dialog_shown = time.time() * 1000

    def __hide_message(self):
        self.dialog_label.place_forget()

    def __show_value(self, value):
        if not self.is_dialog_created:
            self.create_dialog()

        self.show()
        self.dialog_value_label.configure(text=value)
        self.is_dialog_shown = True
        self.last_dialog_shown = time.time() * 1000

    def __show_brightness_icon(self):
        self.brightness_i.place(relx=0.15, rely=0.5, anchor="center")

    def __hide_brightness_icon(self):
        self.brightness_i.place_forget()

    def __show_brightness_progressbar(self):
        self.brightness_progress.place(relx=0.5, rely=0.5, anchor="center")

    def __hide_brightness_progressbar(self):
        self.brightness_progress.place_forget()


if __name__ == "__main__":
    do_nothing = lambda: None
    gui_controller = GuiController(do_nothing)
    
    t = time.time()
    gui_controller.show_general_message("Test message")
    while (time.time() - t) < 1:
        gui_controller.update()
        time.sleep(0.1)

    t = time.time()
    gui_controller.show_brightness(40)
    while (time.time() - t) < 1:
        gui_controller.update()
        time.sleep(0.1)

    gui_controller.quit_window()
