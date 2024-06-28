import time
import getch
from serial import SerialException
from audio_controller import AudioController
from gui_controller import GuiController
from monitor_controller import MonitorController
from serial_controller import SerialController


def handle_frame(frame, monitor_controller, gui_controller, audio_controller):
    d_volume, d_brightness = frame

    if d_brightness != 0:
        monitor_controller.increase_brightness(d_brightness)
        gui_controller.show_brightness_message(
            " Brightness: {}".format(monitor_controller.get_brightness()))

    if d_volume != 0:
        audio_controller.increase_volume(d_volume)
        gui_controller.show_volume_message(
            " Volume: {:.1f}".format(audio_controller.get_volume()))


def main():
    print("Hello world!")
    audio_controller = AudioController()
    gui_controller = GuiController()
    monitor_controller = MonitorController()
    serial_controller = SerialController()

    active = True
    print("active")

    while active:
        try:
            # if msvcrt.kbhit() and getch() == b'r':
            # if getch.getch() == b'r':
            #     print("Resetting audio controller")
            #     gui_controller.show_general_message(
            #         "Resetting audio controller")
            #     audio_controller.reset()
            #     gui_controller.update()
            #     time.sleep(1)
            #     continue
            if serial_controller.is_connected == False:
                serial_controller.connect()
                gui_controller.show_general_message(
                    "Connected to {}".format(serial_controller.serial.name))
            else:
                frame = serial_controller.update()
                if frame != None:
                    handle_frame(frame, monitor_controller,
                                 gui_controller, audio_controller)

                gui_controller.update()
                time.sleep(0.010)  # 10 ms

        except SerialException as e:
            print("Serial exception: {}".format(e))
            serial_controller.disconnect()
            serial_controller.reset()
            gui_controller.show_general_message("Serial disconnected")
            time.sleep(5)

        except Exception as e:
            print("General exception: {}".format(e))
            serial_controller.disconnect()
            active = False

        except KeyboardInterrupt:
            print("Keyboard interrupt")
            serial_controller.disconnect()
            active = False


if __name__ == "__main__":
    main()
