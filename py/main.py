# Main class to control robocar.
import sys
from os.path import dirname, abspath
from tkinter import Tk, Button, Label, StringVar

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from py.echo import Echo

root = Tk()


class Controller:

    def __init__(self, distance_prompt):
        """Initialize class's data here"""
        print("Init  controller")
        self.is_run = False
        self.distance_prompt = distance_prompt
        self.echo = Echo(self.on_echo)

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
        self.distance_prompt.set("Distance: %.1f cm" % distance)


# Quit application
def quit_main(robocar_controller):
    print("Quit main")
    robocar_controller.stop()
    root.destroy()


if __name__ == "__main__":
    print("Robocar started on %s" % py.config.CONFIG)
    distance_prompt = StringVar()

    controller = Controller(distance_prompt)

    root.title("Robocar")
    root.geometry('{}x{}'.format(300, 200))

    start_button = Button(root, text="Start", command=controller.start)
    stop_button = Button(root, text="Stop", command=controller.stop)
    label = Label(root, textvariable=distance_prompt, width=30)

    start_button.pack()
    stop_button.pack()
    label.pack()

    root.protocol("WM_DELETE_WINDOW", lambda: quit_main(controller))
    root.mainloop()

    print("Robocar stopped")
