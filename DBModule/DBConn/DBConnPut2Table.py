import importlib
import os
from DBModule.DBConn.DBConnMainClass import DBConnMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker


class DBConnPut2Table(DBConnMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _engine = None
    __url = None
    model_module = "DBModule.DBMod"

    def __init__(self):
        super().__init__()

    def create_sync_engine(self):
        try:
            from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
            self._engine = DBConnAlchemy().create_alchemy_con_sync()
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    def get_all_tables_list(self):
        self.create_sync_engine()
        inspector = sqlalchemy.inspect(self._engine)
        return inspector.get_table_names()

    def check_table_exist(self, table_name: str = None):
        self.create_sync_engine()
        # res = self._engine.dialect.has_table(self._engine.connect(), table_name=table_name, schema='dbo')
        res = self._engine.dialect.has_table(connection=self._engine.connect(), table_name=table_name)
        return res

    def put_data_dict_2table(self, model_data_dict: dict = None,
                             model_name: str = None):
        inserted_rows_num = 0
        try:
            module_import = importlib.import_module(f"{self.model_module}.{model_name}")
            model_main_class = getattr(module_import, model_name)
            self.create_sync_engine()
            model_new_obj = model_main_class(**model_data_dict)
            Session = sessionmaker(bind=self._engine)
            session = Session()
            # check is presence position?
            session.add(model_new_obj)
            inserted_rows_num += 1
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num, "updated": 0})

    def put_data_dict_2table_with_update(self, table_name: str = None,
                                         model_data_dict: dict = None,
                                         model_class_name: str = None,
                                         unique_col_name: str = None):
        """ deprecated! """
        inserted_rows_num = 0
        updated_rows_num = 0
        today = datetime.datetime.now()
        try:
            module = importlib.import_module(f"{self.model_module}.{model_class_name}")
            model_class = getattr(module, model_class_name)
            self.create_sync_engine()
            new_model_obj = model_class(**model_data_dict)
            Session = sessionmaker(bind=self._engine)
            session = Session()
            # check is presence position?
            qry_object = session.query(model_class).where(
                getattr(model_class, unique_col_name) == getattr(new_model_obj, unique_col_name))
            if qry_object.first() is None:
                session.add(new_model_obj)
                inserted_rows_num += 1
                # print(f"added client {new_cust_bal_row.counterparty.get('name')}")
            else:
                qry_object.update(model_data_dict)
                updated_rows_num += 1
                # print(f"updated client {new_cust_bal_row.counterparty.get('name')}")
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num, "updated": updated_rows_num})


if __name__ == '__main__':
    connector = DBConnPut2Table()
    # print(connector.create_engine())
    print(connector.get_all_tables_list())
    print(connector.check_table_exist('detect_model'))
    today = datetime.datetime.now()
    data_dict = dict({"created": today,
                      "category_name": "person",
                      "confident": 56.01,
                      "box_x1": 10.02,
                      "box_y1": 15.03,
                      "box_x2": 20.04,
                      "box_y2": 25.05,
                      "frame_width": 640,
                      "frame_height": 380,
                      "path": "/temp",
                      "description": "test write"
                      })
    model_class_name = "DBModDetect"
    connector.put_data_dict_2table(model_data_dict=data_dict,
                                   model_name=model_class_name,
                                   )

    # how to create class from classname
    module = importlib.import_module("DBModule.DBMod.DBModDetect")
    model_class = getattr(module, model_class_name)
    new_model_obj = model_class(**data_dict)
    print(new_model_obj.description)
