from sqlalchemy import select

from database import models


class Config:
    @staticmethod
    def get_fields(table):
        table_fields = {
            "buyers": ["№", "ФИО"],
            "managers": ["№", "ФИО"],
            "cars": ["№", "Марка"],
            "sales": ["№", "№ менеджера", "№ автомобиля", "Государственный номер", "№ покупателя", "Дата", "Цена"],
            "average_transaction": ["Сумма"],
            "share_sales_car": ["№ автомобиля", "Доля (%)"]
        }

        return table_fields[table]

    @staticmethod
    def get_table_fields(table):
        table_field_models = {
            "buyers": {
                "default": models.Buyer,
                "full_name": models.Buyer.full_name
            },
            "managers": {
                "default": models.Manager,
                "full_name": models.Manager.full_name
            },
            "cars": {
                "default": models.Car,
                "model": models.Car.model
            },
            "sales": {
                "default": models.Sale,
                "manager_id": models.Sale.manager_id,
                "car_id": models.Sale.car_id,
                "state_number": models.Sale.state_number,
                "buyer_id": models.Sale.buyer_id,
                "date": models.Sale.date,
                "price": models.Sale.price
            }
        }

        return table_field_models[table]

    def get_output_templates(self, database, select_table, select_extension, select_output_type):
        stmt = select(self.get_table_fields(select_table)["default"])

        output_templates = {
            "JSON": {
                "Средняя сумма сделки": (database.get_average_transaction(), self.get_fields("average_transaction")),

                "Доля продаж автомобилей разных марок": (database.get_share_sales_car(),
                                                         self.get_fields("share_sales_car")),

                "Таблица": (database.select_query(stmt, 3), self.get_fields(select_table))
            },
            "EXCEL": {
                "Средняя сумма сделки": (database.get_average_transaction(), "Средняя сумма сделки",
                                         self.get_fields("average_transaction")),

                "Доля продаж автомобилей разных марок": (database.get_share_sales_car(),
                                                         "Доля продаж автомобилей",
                                                         self.get_fields("share_sales_car")),

                "Таблица": (database.select_query(stmt, 3), "Таблица",
                            self.get_fields(select_table))
            }
        }

        return output_templates[select_extension][select_output_type]
