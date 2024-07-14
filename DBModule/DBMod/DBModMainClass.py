from DBModule.DBMainClass import DBMainClass
import os
import sqlite3


class DBModMainClass(DBMainClass):
    """ main class for models packages"""
    logger_name = f"{os.path.basename(__file__)}"


    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = DBModMainClass()
    connect.logger.info("testing DBModMainClass")

