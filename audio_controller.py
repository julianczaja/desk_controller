import time

import win32con
import win32api

UPDATE_INTERVAL_MS = 20

class AudioController:
    def __init__(self):
        self.last_volume_change = time.time() * 1000

    def change_volume(self, d_volume):
        t_now = time.time() * 1000
        d_time = t_now - self.last_volume_change

        if d_time > UPDATE_INTERVAL_MS:
            if (d_volume > 0):
                for _ in range(d_volume):
                    self.__increase_volume()
            else:
                for _ in range(-d_volume):
                    self.__decrease_volume()

            self.last_volume_change = time.time() * 1000

    def __increase_volume(self):
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)

    def __decrease_volume(self):
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
