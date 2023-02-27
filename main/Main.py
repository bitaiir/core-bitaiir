# Imports
from functions.Debug import Debug
from core.Core import Core

class Main:

    def startCore(self):
        # Objects
        core = Core()

        # Start
        core.init()
        Debug.log("Starting Core.")



if __name__ == '__main__':
    main = Main()
    main.startCore()
