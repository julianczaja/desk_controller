import alsaaudio
import time

UPDATE_INTERVAL_MS = 70


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class AudioController:
    def __init__(self):
        self.mixer = alsaaudio.Mixer('Master')
        self.volume = self.mixer.getvolume()[0]

        self.last_volume = self.volume
        self.last_volume_change = time.time() * 1000

    def reset(self):
        self.__init__()

    def increase_volume(self, d_volume):
        t_now = time.time() * 1000

        #self.volume = clamp(self.volume + (d_volume / 2.0), 0.0, 100.0)
        self.volume = clamp(self.volume + d_volume, 0.0, 100.0)
        d_time = t_now - self.last_volume_change

        if d_time > UPDATE_INTERVAL_MS and self.last_volume != self.volume:
            self.set_volume()
            self.last_volume_change = time.time() * 1000
            self.last_volume = self.volume

    def set_volume(self): # 0-100 int
        self.mixer.setvolume(int(self.volume))

    def get_volume(self): # 0-100 int
        return self.mixer.getvolume()[0]


if __name__ == "__main__":
    audio_controller = AudioController()
    vol = audio_controller.get_volume()
    print("Current volume: {}".format(vol))
