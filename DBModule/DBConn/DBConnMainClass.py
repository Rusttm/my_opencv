from DBModule.DBMainClass import DBMainClass
import os
import sqlite3


class DBConnMainClass(DBMainClass):
    """ mainclass for database connections
    also creates new sqlite db """
    logger_name = f"{os.path.basename(__file__)}"
    db_sqlite_dir = "sqlite_db"
    db_sqlite_name = "sqlite_db.db"

    def __init__(self):
        # print("test class")
        super().__init__()

    def create_sqlite_db(self, name: str = None):
        """ creates new sqlite db"""
        if name is None:
            name = self.db_sqlite_name
        upper_dir = os.path.dirname(os.path.dirname(__file__))
        sqlite_db_full_path = os.path.join(upper_dir, self.db_sqlite_dir, name)
        connection = sqlite3.connect(sqlite_db_full_path)
        connection.close()


if __name__ == "__main__":
    connect = DBConnMainClass()
    connect.logger.info("testing MainClass")
    connect.create_sqlite_db()
