from AiogramPackage.TGConnectors.BOTPkgLogger import BOTPkgLogger
from AiogramPackage.TGConnectors.BOTReadJsonAsync import BOTReadJsonAsync
import os


class BOTMainClass(BOTPkgLogger, BOTReadJsonAsync):
    logger_name = f"{os.path.basename(__file__)}"

    def __init__(self):
        super().__init__()
        BOTReadJsonAsync.__init__(self)

    def python_version_checker(self):
        import sys
        print(f"You work on Python v {sys.version_info[0:3]}")
        if sys.version_info[0:3] != (3, 10, 10):
            msg = f"Python version {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} it is not 10, please use Python3v10.10"
            self.logger.debug(msg)


if __name__ == "__main__":
    connect = BOTMainClass()
    connect.logger.info("testing MainClass")
    connect.python_version_checker()
    print(connect._config_data)
