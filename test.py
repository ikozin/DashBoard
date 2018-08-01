import urllib.request as request
import urllib.parse as parse

class Mainboard:

    def __init__(self):
        """ """
        pass

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""
        pass


    def loop(self):
        pass


if __name__ == "__main__":

    print(pygame.version.ver)
    app = Mainboard()
    app.loop()
    sys.exit(0)
