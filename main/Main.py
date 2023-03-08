# Imports
from tools.Debug import Debug
from core.Core import Core


class Main:

    def run(self):
        # Objects
        core = Core()

        # Start
        core.init()


if __name__ == '__main__':
    main = Main()
    main.run()
