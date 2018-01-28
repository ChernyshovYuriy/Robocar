import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import py.config
from tkinter import Tk, Button, Label


class UiCommander:

    def __init__(self, controller_in, root_in, distance_prompt_in, motors_prompt_in):
        print("Init  ui commander on %s" % py.config.CONFIG)
        self.controller_ref = controller_in
        self.distance_prompt_ref = distance_prompt_in
        self.motors_prompt_ref = motors_prompt_in

        self.root = root_in
        self.root.title("Robocar")
        self.root.geometry('{}x{}'.format(400, 200))
        self.root.grid()

        start_button = Button(self.root, text="Start", command=self.controller_ref.start, width=22)
        stop_button = Button(self.root, text="Stop", command=self.controller_ref.stop, width=22)
        distance_label = Label(self.root, textvariable=self.distance_prompt_ref)
        motors_label = Label(self.root, textvariable=self.motors_prompt_ref)

        start_button.grid(column=0, row=0)
        stop_button.grid(column=1, row=0)
        distance_label.grid(column=0, row=1)
        motors_label.grid(column=1, row=1)

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit_main())
        self.root.mainloop()

    # Quit application
    def quit_main(self):
        print("Quit main")
        self.controller_ref.stop()
        self.root.destroy()