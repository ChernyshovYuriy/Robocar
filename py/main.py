# Main class to control robocar.
import sys
from os.path import dirname, abspath
from tkinter import Tk, Button, Label, StringVar

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from py.echo import Echo
from py.motors import Motors
from py.gpio_manager import GPIOManager

root = Tk()


class Controller:

    def __init__(self, distance_prompt_in, motors_prompt_in):
        print("Init  controller on %s" % py.config.CONFIG)
        self.is_run = False
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in
        self.echo = Echo(self.on_echo)
        self.motors = Motors(
            self.on_motors_stopped, self.on_motors_started, self.on_motors_turning()
        )

    # Start controller.
    def start(self):
        if self.is_run is True:
            return

        print("Start controller")
        self.echo.start()
        self.is_run = True

    # Stop controller
    def stop(self):
        if self.is_run is False:
            return

        print("Stop  controller")
        self.echo.stop()
        self.is_run = False

    # Callback function to echo class
    def on_echo(self, distance):
        print(" -- echo: %s" % distance)
        self.distance_prompt_ref.set("Distance: %.1f cm" % distance)
        self.motors.on_echo(distance)

    def on_motors_stopped(self):
        print(" -- motors stopped")
        self.motors_prompt_ref.set("Motors stopped")

    def on_motors_started(self):
        print(" -- motors started")
        self.motors_prompt_ref.set("Motors started")

    def on_motors_turning(self):
        print(" -- motors turning")
        self.motors_prompt_ref.set("Motors Turning")


# Quit application
def quit_main(robocar_controller):
    print("Quit main")
    robocar_controller.stop()
    root.destroy()


if __name__ == "__main__":
    print("Robocar started on %s" % py.config.CONFIG)
    GPIOManager.init()

    distance_prompt = StringVar()
    motors_prompt = StringVar()

    controller = Controller(distance_prompt, motors_prompt)

    root.title("Robocar")
    root.geometry('{}x{}'.format(400, 200))
    root.grid()

    start_button = Button(root, text="Start", command=controller.start, width=22)
    stop_button = Button(root, text="Stop", command=controller.stop, width=22)
    distance_label = Label(root, textvariable=distance_prompt)
    motors_label = Label(root, textvariable=motors_prompt)

    start_button.grid(column=0, row=0)
    stop_button.grid(column=1, row=0)
    distance_label.grid(column=0, row=1)
    motors_label.grid(column=1, row=1)

    root.protocol("WM_DELETE_WINDOW", lambda: quit_main(controller))
    root.mainloop()

    GPIOManager.cleanup()

    print("Robocar stopped")
