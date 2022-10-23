from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from numpy import interp
import time

UPDATE_INTERVAL_MS = 20


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class AudioController:
    def __init__(self):
        speakers = AudioUtilities.GetSpeakers()
        interface = speakers.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume = self.get_volume()

        self.last_volume = self.volume
        self.last_volume_change = time.time() * 1000

    def reset(self):
        self.__init__()

    def increase_volume(self, d_volume):
        t_now = time.time() * 1000

        self.volume = clamp(self.volume + (d_volume / 2.0), 0.0, 100.0)
        d_time = t_now - self.last_volume_change

        if d_time > UPDATE_INTERVAL_MS and self.last_volume != self.volume:
            self.set_volume()
            self.last_volume_change = time.time() * 1000
            self.last_volume = self.volume

    def set_volume(self):  # 0-100 float
        new_volume = self.volume / 100.0
        self.volume_controller.SetMasterVolumeLevelScalar(new_volume, None)

    def get_volume(self):  # 0-100 float
        return self.volume_controller.GetMasterVolumeLevelScalar() * 100.0


if __name__ == "__main__":
    audio_controller = AudioController()
    vol = audio_controller.get_volume()
    print("Current volume: {}".format(vol))
