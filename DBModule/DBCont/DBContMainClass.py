from DBModule.DBMainClass import DBMainClass
import os


class DBContMainClass(DBMainClass):
    """ mainclass for database controllers """
    logger_name = f"{os.path.basename(__file__)}"
    db_sqlite_dir = "sqlite_db"
    db_sqlite_name = "sqlite_db.db"

    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = DBContMainClass()
    connect.logger.info("testing MainClass")

