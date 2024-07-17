import time
from serial import SerialException
from audio_controller import AudioController
from gui_controller import GuiController
from monitor_controller import MonitorController
from serial_controller import SerialController

global active


def handle_frame(
    frame,
    monitor_controller: MonitorController,
    gui_controller: GuiController,
    audio_controller: AudioController,
):
    d_volume, d_brightness = frame

    if d_brightness != 0:
        monitor_controller.increase_brightness(d_brightness)
        gui_controller.show_brightness(monitor_controller.get_brightness())

    if d_volume != 0:
        audio_controller.change_volume(d_volume)


def gui_exit_callback():
    print("gui_exit_callback")
    global active
    active = False

def main():
    global active
    active = True

    audio_controller = AudioController()
    gui_controller = GuiController(exit_callback=gui_exit_callback)
    monitor_controller = MonitorController()
    serial_controller = SerialController()

    while active:
        try:
            if serial_controller.is_connected == False:
                serial_controller.connect()
                gui_controller.show_general_message(
                    "Connected to {}".format(serial_controller.serial.name)
                )
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
            gui_controller.exit()


if __name__ == "__main__":
    main()
