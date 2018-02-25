import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import contextlib
import termios
import py.config

# 101 - e
ENG_FWD = 101
# 100 - c
ENG_BWD = 99
# 100 - d
ENG_OFF = 100
# 119 - w
START = 119
# 115 - s
STOP = 115
# 113 - q
QUIT = 113


# Implementation of the commander based on the command line - events from the keyboard.
class CmdCommander:

    def __init__(self, controller_in):
        print("Init  cmd commander on %s" % py.config.CONFIG)
        self.controller_ref = controller_in

        with self.raw_mode(sys.stdin):
            try:
                while True:
                    ch = sys.stdin.read(1)
                    print('%s' % ord(ch))
                    if not ch or ord(ch) == START:
                        self.controller_ref.start()
                    if not ch or ord(ch) == STOP:
                        self.controller_ref.stop()
                    if not ch or ord(ch) == QUIT:
                        self.controller_ref.stop()
                    if not ch or ord(ch) == ENG_FWD:
                        self.controller_ref.eng_fwd()
                    if not ch or ord(ch) == ENG_BWD:
                        self.controller_ref.eng_bwd()
                    if not ch or ord(ch) == ENG_OFF:
                        self.controller_ref.stop()
                        break
            except (KeyboardInterrupt, EOFError):
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