import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import contextlib
import termios
import py.config


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
                    # 119 - w
                    # 115 - s
                    # 113 - q
                    if not ch or ord(ch) == 119:
                        self.controller_ref.start()
                    if not ch or ord(ch) == 115:
                        self.controller_ref.stop()
                    if not ch or ord(ch) == 113:
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