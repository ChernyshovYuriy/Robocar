import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import contextlib
import termios

# w
ENG_FWD = 119
# x
ENG_BWD = 120
# a
ENG_TURN_L = 97
# d
ENG_TURN_R = 100
# s
ENG_OFF = 115
# Enter
START = 10
# Space
STOP = 32
# Print echo
TRIGGER_PRINT_ECHO = 101
# Esc
QUIT = 27


# Implementation of the commander based on the command line - events from the keyboard.
class CmdCommander:

    def __init__(self, controller_in):
        print("Init  cmd commander")
        self.controller_ref = controller_in

        with self.raw_mode(sys.stdin):
            try:
                while True:
                    ch = sys.stdin.read(1)
                    print('Key %s pressed' % ord(ch))
                    if not ch or ord(ch) == START:
                        self.controller_ref.start()
                    if not ch or ord(ch) == STOP:
                        self.controller_ref.stop()
                    if not ch or ord(ch) == ENG_FWD:
                        self.controller_ref.eng_fwd()
                    if not ch or ord(ch) == ENG_BWD:
                        self.controller_ref.eng_bwd()
                    if not ch or ord(ch) == ENG_TURN_L:
                        self.controller_ref.eng_turn_l()
                    if not ch or ord(ch) == ENG_TURN_R:
                        self.controller_ref.eng_turn_r()
                    if not ch or ord(ch) == ENG_OFF:
                        self.controller_ref.eng_stop()
                    if not ch or ord(ch) == TRIGGER_PRINT_ECHO:
                        self.controller_ref.trigger_print_echo()
                    if not ch or ord(ch) == QUIT:
                        self.controller_ref.stop()
                        break
            except (KeyboardInterrupt, EOFError):
                print("KeyboardInterrupt error, %s" % EOFError)
                self.controller_ref.stop()
                pass

    @contextlib.contextmanager
    def raw_mode(self, file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)