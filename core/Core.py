# Imports
from tools.Debug import Debug
import pyfiglet


class Core:

    def __init__(self):
        # Show logo;
        self.show_logo()

    def show_logo(self):
        # Vars.
        ascii_logo = pyfiglet.figlet_format("bitaiir", font="banner3-D")

        # Debug;
        Debug.art_ascii(ascii_logo)

    def init(self):
        print("Core Init")
