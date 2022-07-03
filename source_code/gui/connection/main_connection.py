from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import models
from gui.windows import main_window


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, database, config, utils, excel):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.database = database
        self.config = config
        self.utils = utils
        self.excel = excel

        self.add_table.clicked.connect(self.show_add_page)
        self.open_table.clicked.connect(self.show_table)
        self.change_table.clicked.connect(self.show_choice_page)

        self.back_button.clicked.connect(self.to_back_page)
        self.back_button_2.clicked.connect(self.to_back_page)
        self.back_button_3.clicked.connect(self.to_back_page)
        self.back_button_4.clicked.connect(self.to_back_page)
        self.back_button_5.clicked.connect(self.to_back_page)
        self.back_button_6.clicked.connect(self.to_back_page)
        self.back_button_7.clicked.connect(self.to_back_page)
        self.back_button_8.clicked.connect(self.to_back_page)

        self.select_table.clear()
        self.select_table.addItems(self.database.get_tables_name())

        self.add_buyer_button.clicked.connect(self.add_elements)
        self.add_manager_button.clicked.connect(self.add_elements)
        self.add_car_button.clicked.connect(self.add_elements)
        self.add_sale_button.clicked.connect(self.add_elements)

        self.delete_table.clicked.connect(self.fill_list)
        self.delete_button.clicked.connect(self.delete_by_id)

        self.open_change.clicked.connect(self.show_change_page)
        self.change_button.clicked.connect(self.change_elements)

        self.save_table.clicked.connect(self.show_output_page)
        self.output_button.clicked.connect(self.output_to_file)

    def to_back_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_output_page(self):
        self.stackedWidget.setCurrentIndex(8)

    def output_to_file(self):
        select_extension = self.select_extension.currentText()
        select_output_type = self.select_output_type.currentText()
        select_table = self.select_table.currentText()
        output_templates = self.config.get_output_templates(self.database, select_table, select_extension,
                                                            select_output_type)

        if select_extension == "EXCEL":
            self.output_to_excel(*output_templates)
        elif select_extension == "JSON":
            self.output_to_json(*output_templates)

    def output_to_json(self, data_from_database, fields):
        data = []

        for row in data_from_database:
            data.append({key: value for key, value in zip(tuple(fields), row)})

        file_path = QFileDialog.getOpenFileName(self, "Выбор JSON-файла", "./", "Image(*.json)")[0]

        if file_path:
            self.utils.save_to_json(file_path, data)
            self.stackedWidget.setCurrentIndex(0)

    def output_to_excel(self, data_from_database, header, fields):
        self.excel.create_workbook()
        file_path = QFileDialog.getOpenFileName(self, "Выбор EXCEL-файла", "./", "Image(*.xlsx)")[0]

        if file_path:
            self.excel.sheet.title = header
            self.excel.sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(data_from_database[0]))

            self.excel.sheet["A1"] = header
            self.excel.set_sheet_styles(1)

            self.excel.sheet.append(fields)
            self.excel.set_sheet_styles(2)

            for index, value in enumerate(data_from_database, 3):
                self.excel.sheet.append(tuple(map(str, value)))

                for cell in self.excel.sheet[index]:
                    cell.border = self.excel.full_border
                    cell.alignment = self.excel.alignment_center

            try:
                self.excel.workbook.save(filename=file_path)
                self.stackedWidget.setCurrentIndex(0)
            except PermissionError:
                QMessageBox.warning(self, "ОШИБКА", "Закройте выбранный файл")

    def change_elements(self):
        table = self.config.get_table_fields(self.select_table.currentText())
        type_change = table[self.type_change.currentText()]
        id_change = int(self.id_change.currentText())
        new_change = self.new_change.toPlainText()

        with Session(self.database.engine) as session:
            session.query(table["default"]).filter(table["default"].id == id_change).update({type_change: new_change})
            session.commit()
        self.stackedWidget.setCurrentIndex(0)

    def show_change_page(self):
        self.id_select_change.clear()
        self.type_select_change.clear()
        self.new_change.clear()

        id_change = self.id_change.currentText()
        select_table = self.select_table.currentText()
        type_change = self.type_change.currentText()
        current_table = self.config.get_table_fields(select_table)
        new_change_text = self.database.select_query(select(current_table[type_change]
                                                            ).where(current_table["default"].id == id_change), 2)

        self.new_change.setText(str(new_change_text))
        self.id_select_change.setText(f"ID: {id_change}")
        self.type_select_change.setText(f"Изменяемое поле: {type_change}")

        self.stackedWidget.setCurrentIndex(7)

    def show_choice_page(self):
        self.id_change.clear()
        self.type_change.clear()

        select_table = self.select_table.currentText()
        current_table = self.config.get_table_fields(select_table)["default"]

        ids = [str(index) for index in self.database.select_query(select(current_table.id), 1)]
        types = [column.key for column in current_table.__table__.columns if column.key.find("id") == -1]

        self.id_change.addItems(ids)
        self.type_change.addItems(types)

        self.stackedWidget.setCurrentIndex(6)

    def delete_by_id(self):
        select_table = self.select_table.currentText()
        current_table = self.config.get_table_fields(select_table)["default"]
        id_input_delete = self.id_input_delete.text()

        self.database.engine_connect(delete(current_table).where(current_table.id == id_input_delete))
        self.stackedWidget.setCurrentIndex(0)

    def fill_list(self):
        self.id_list_delete.clear()

        select_table = self.select_table.currentText()
        current_table = self.config.get_table_fields(select_table)["default"]

        self.id_list_delete.addItems([str(index) for index in self.database.select_query(select(current_table.id), 1)])
        self.stackedWidget.setCurrentIndex(5)

    def show_table(self):
        if self.select_table.currentText() in ["buyers", "managers"]:
            table_model = self.config.get_table_fields(self.select_table.currentText())["default"]
            self.table_data.clear()

            ids = self.database.select_query(select(table_model.id), 1)
            full_names = self.database.select_query(select(table_model.full_name), 1)

            self.table_data.setColumnCount(2)
            self.table_data.setRowCount(len(ids))

            self.utils.fill_table(self.table_data, ids, 0)
            self.utils.fill_table(self.table_data, full_names, 1)

        elif self.select_table.currentText() == "cars":
            self.table_data.clear()

            ids = self.database.select_query(select(models.Car.id), 1)
            models_car = self.database.select_query(select(models.Car.model), 1)

            self.table_data.setColumnCount(2)
            self.table_data.setRowCount(len(ids))

            self.utils.fill_table(self.table_data, ids, 0)
            self.utils.fill_table(self.table_data, models_car, 1)

        elif self.select_table.currentText() == "sales":
            self.table_data.clear()

            ids = self.database.select_query(select(models.Sale.id), 1)
            manager_ids = self.database.select_query(select(models.Sale.manager_id), 1)
            car_ids = self.database.select_query(select(models.Sale.car_id), 1)
            state_numbers = self.database.select_query(select(models.Sale.state_number), 1)
            buyer_ids = self.database.select_query(select(models.Sale.buyer_id), 1)
            dates = self.database.select_query(select(models.Sale.date), 1)
            prices = self.database.select_query(select(models.Sale.price), 1)

            self.table_data.setColumnCount(7)
            self.table_data.setRowCount(len(ids))

            self.utils.fill_table(self.table_data, ids, 0)
            self.utils.fill_table(self.table_data, manager_ids, 1)
            self.utils.fill_table(self.table_data, car_ids, 2)
            self.utils.fill_table(self.table_data, state_numbers, 3)
            self.utils.fill_table(self.table_data, buyer_ids, 4)
            self.utils.fill_table(self.table_data, dates, 5)
            self.utils.fill_table(self.table_data, prices, 6)

    def show_add_page(self):
        if self.select_table.currentText() == "buyers":
            self.id_buyer.clear()
            self.full_name_buyer.clear()

            self.id_buyer.setText(self.database.get_last_index(models.Buyer.id))

            self.stackedWidget.setCurrentIndex(1)

        elif self.select_table.currentText() == "managers":
            self.id_manager.clear()
            self.full_name_manager.clear()

            self.id_manager.setText(self.database.get_last_index(models.Manager.id))

            self.stackedWidget.setCurrentIndex(2)

        elif self.select_table.currentText() == "cars":
            self.id_car.clear()
            self.model_car.clear()

            self.id_car.setText(self.database.get_last_index(models.Car.id))

            self.stackedWidget.setCurrentIndex(3)

        elif self.select_table.currentText() == "sales":
            self.id_sale.clear()
            self.id_manager_sale.clear()
            self.id_car_sale.clear()
            self.state_number_sale.clear()
            self.id_buyer_sale.clear()
            self.price_sale.clear()

            self.id_sale.setText(self.database.get_last_index(models.Sale.id))
            self.id_manager_sale.addItems(self.database.select_query(select(models.Manager.full_name), 1))
            self.id_car_sale.addItems(self.database.select_query(select(models.Car.model), 1))
            self.id_buyer_sale.addItems(self.database.select_query(select(models.Buyer.full_name), 1))

            self.stackedWidget.setCurrentIndex(4)

    def add_elements(self):
        try:
            if self.select_table.currentText() == "buyers":
                id_buyer = self.id_buyer.text()
                full_name = self.full_name_buyer.text()

                self.database.insert_query(models.Buyer, id_buyer, full_name)
                self.stackedWidget.setCurrentIndex(0)
                self.show_table()

            elif self.select_table.currentText() == "managers":
                id_manager = self.id_manager.text()
                full_name = self.full_name_manager.text()

                self.database.insert_query(models.Manager, id_manager, full_name)
                self.stackedWidget.setCurrentIndex(0)
                self.show_table()

            elif self.select_table.currentText() == "cars":
                id_patient = self.id_car.text()
                model = self.model_car.text()

                self.database.insert_query(models.Car, id_patient, model)
                self.stackedWidget.setCurrentIndex(0)
                self.show_table()

            elif self.select_table.currentText() == "sales":
                id_sale = self.id_sale.text()

                id_manager = int(self.database.select_query(
                    select(models.Manager.id).where(models.Manager.full_name == self.id_manager_sale.currentText()), 2))

                id_car = int(self.database.select_query(
                    select(models.Car.id).where(models.Car.model == self.id_car_sale.currentText()), 2))

                id_buyer = int(self.database.select_query(
                    select(models.Buyer.id).where(models.Buyer.full_name == self.id_buyer_sale.currentText()), 2))

                state_number = self.state_number_sale.text()
                date = self.date_sale.text()
                price = self.price_sale.text()

                self.database.insert_query(models.Sale, id_sale, id_manager, id_car,
                                           state_number, id_buyer, date, price)

                self.stackedWidget.setCurrentIndex(0)
                self.show_table()
        except TypeError:
            QMessageBox.warning(self, "ОШИБКА", "Заполните все поля")
