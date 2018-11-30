#!/usr/bin/env python3

import platform
from os import getcwd


def main():
    import gui
    # Initialize GUI
    instanced_gui = gui.D3Edit()
    instanced_gui.start()


if __name__ == "__main__":
    venv_platforms = ['Linux', 'Darwin']
    running_os = platform.system()
    # activate Linux/Darwin venvs:
    if any(p in running_os for p in venv_platforms):
        print("activated linux venv")
        activate_this_file = "{}/venv/bin/activate_this.py".format(getcwd())
        exec(open(activate_this_file).read(), dict(__file__=activate_this_file))
    elif running_os == 'Windows':
        print("Activating Windows venv")
        activate_this_file = "{}\\winvenv\\Scripts\\activate_this.py".format(getcwd())
        exec(open(activate_this_file).read(), dict(__file__=activate_this_file))
    main()
