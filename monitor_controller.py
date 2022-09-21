from monitorcontrol import get_monitors
import time


UPDATE_INTERVAL_MS = 70

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class MonitorController:

    def __init__(self):
        self.monitor = get_monitors()[0]

        with self.monitor:
            self.brightness = self.monitor.get_luminance()
            self.last_brightness = self.brightness
            self.last_brightness_change = time.time() * 1000

    def increase_brightness(self, d_brightness):
        self.brightness = clamp(self.brightness + d_brightness, 0, 100)

        t_now = time.time() * 1000
        d_time = t_now - self.last_brightness_change

        if d_time > UPDATE_INTERVAL_MS and self.last_brightness != self.brightness:
            with self.monitor:
                self.monitor.set_luminance(self.brightness)
                self.last_brightness_change = time.time() * 1000
                self.last_brightness = self.brightness

    def get_brightness(self):
        return self.brightness