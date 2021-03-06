import os
from itertools import chain

from sqlalchemy import create_engine, MetaData, insert, select, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from database import models


class DataBase:
    def __init__(self, name):
        self.name = name
        self.metadata = MetaData()
        self.engine = create_engine(f"sqlite:///{name}.sqlite3")

    @staticmethod
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def delete_database(self):
        if os.path.exists(self.name):
            os.remove(self.name)

    def create_all_tables(self):
        if not os.path.exists(self.name):
            models.Base.metadata.create_all(self.engine)

    def engine_connect(self, query, isReturn=False):
        with self.engine.connect() as connection:
            if isReturn:
                return connection.execute(query)
            connection.execute(query)

    def select_query(self, query, return_type: int):
        with self.engine.connect() as connection:
            if return_type == 1:
                return list(chain.from_iterable(connection.execute(query).fetchall()))
            elif return_type == 2:
                return connection.execute(query).fetchone()[0]
            elif return_type == 3:
                return connection.execute(query).fetchall()

    def insert_query(self, table, *args):
        self.engine_connect(insert(table).values(args))

    def get_last_index(self, table):
        try:
            index = str(sorted(self.select_query(select(table), 1))[-1] + 1)
        except IndexError:
            index = str(0)
        return index

    def get_tables_name(self):
        return self.engine.table_names()

    def get_session(self, query):
        with Session(self.engine) as session:
            session.query(query)
            session.commit()

    def get_average_transaction(self):
        with Session(self.engine) as session:
            return session.query(func.avg(models.Sale.price)).all()

    def get_share_sales_car(self):
        with Session(self.engine) as session:
            return (session.query(models.Sale.car_id,
                                  func.count(models.Sale.car_id) * 1.0 /
                                  session.query(func.count(models.Sale.id)) * 100
                                  ).group_by(models.Sale.car_id)).all()
