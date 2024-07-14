from DBModule.DBMainLogger import DBMainLogger
import os
class DBMainClass(DBMainLogger):
    logger_name = f"{os.path.basename(__file__)}"
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = DBMainClass()
    connect.logger.info("testing MainClass")
