import time
from audio_controller import AudioController
from gui_controller import GuiController
from monitor_controller import MonitorController
from serial_controller import SerialController


def handle_frame(frame, monitor_controller, gui_controller, audio_controller):
    d_volume, d_brightness = frame

    if d_brightness != 0:
        monitor_controller.increase_brightness(d_brightness)
        gui_controller.show_message("Brightness: {}".format(
            monitor_controller.get_brightness()))

    if d_volume != 0:
        audio_controller.increase_volume(d_volume)
        gui_controller.show_message(
            "Volume: {:.1f}".format(audio_controller.get_volume()))


def main():
    try:
        audio_controller = AudioController()
        gui_controller = GuiController()
        monitor_controller = MonitorController()
        serial_controller = SerialController()

        while True:
            frame = serial_controller.update()
            if frame != None:
                handle_frame(frame, monitor_controller,
                             gui_controller, audio_controller)

            gui_controller.update()
            time.sleep(0.010)  # 10 ms

    except Exception as e:
        print(e)
        serial_controller.close()


if __name__ == "__main__":
    main()
