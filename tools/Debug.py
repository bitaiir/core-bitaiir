class Debug:

    def log(self):
        print("[DEBUG]: {0}\n".format(str(self)))

    def error(self):
        print("[ERROR]: {0}\n".format(str(self)))

    def info(self):
        print("="*50)
        print("{0}".format(str(self)))
        print("="*50)

    def art_ascii(self):
        print("\n")
        print("{0}".format(str(self)))
        print("\n")
