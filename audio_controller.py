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
        interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

        volume_range = self.volume_controller.GetVolumeRange()
        self.volume_range = [float(volume_range[0]), float(volume_range[1])]
        self.volume = self.get_volume()

        self.last_volume = self.volume
        self.last_volume_change = time.time() * 1000

    def increase_volume(self, d_volume):  # volume 0-100 float
        t_now = time.time() * 1000
        self.volume = clamp(self.volume + (d_volume / 5.0), 0.0, 100.0)
        d_time = t_now - self.last_volume_change

        if d_time > UPDATE_INTERVAL_MS and self.last_volume != self.volume:
            mapped_volume = interp(self.volume, [0, 100], self.volume_range)
            self.volume_controller.SetMasterVolumeLevel(mapped_volume, None)
            self.last_volume_change = time.time() * 1000
            self.last_volume = self.volume

    def get_volume(self):  # 0-100 float
        volume = self.volume_controller.GetMasterVolumeLevel()
        return interp(volume, self.volume_range, [0, 100])
