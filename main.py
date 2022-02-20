import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QMessageBox


GET_QUERY = """SELECT *
    FROM CoffeeKinds
    ORDER BY CoffeeKinds.id"""

ADD_QUERY = """INSERT
    INTO CoffeeKinds({})
    VALUES ({})"""

EDIT_QUERY = """UPDATE CoffeeKinds
    SET {}
    WHERE CoffeeKinds.id = ?"""

DEL_QUERY = """DELETE
    FROM CoffeeKinds
    WHERE CoffeeKinds.id = ?"""


class CoffeeAddEdit(QDialog):
    def __init__(self, data=None):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        if data:
            self.le_name.setText(data[0])
            self.le_burnlvl.setText(str(data[1]))
            self.le_beans.setText(str(data[2]))
            self.le_descr.setText(data[3])
            self.le_price.setText(str(data[4]))
            self.le_vol.setText(str(data[5]))

    def get_result(self):
        data = [
            self.le_name.text(),
            int(self.le_burnlvl.text()),
            int(self.le_beans.text()),
            self.le_descr.text(),
            int(self.le_price.text()),
            int(self.le_vol.text()),
        ]
        return data


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        res = self.cursor.execute(GET_QUERY).fetchall()
        self.field_names = [f[0] for f in self.cursor.description]
        for i in range(7):
            title = QTableWidgetItem()
            title.setText(self.field_names[i])
            self.tbl.setHorizontalHeaderItem(i, title)
        self.b_add.clicked.connect(self.add_rec)
        self.b_edit.clicked.connect(self.edit_rec)
        self.b_delete.clicked.connect(self.delete_rec)

    def add_rec(self):
        dlg = CoffeeAddEdit()
        if dlg.exec():
            data = dlg.get_result()
            query = ADD_QUERY.format(
                ", ".join(self.field_names[1:]), ", ".join(["?"] * len(self.field_names[:-1]))
            )
            self.cursor.execute(query, data)
            self.connection.commit()
            self.draw_table()

    def edit_rec(self):
        row_num = self.tbl.currentRow()
        cur_fields = []
        for i in range(1, self.tbl.columnCount()):
            cur_fields.append(self.tbl.item(row_num, i).text())
        dlg = CoffeeAddEdit(cur_fields)
        if dlg.exec():
            data = dlg.get_result()
            query = EDIT_QUERY.format(
                ", ".join(
                    [
                        "{} = '{}'".format(item[0], item[1])
                        for item in zip(self.field_names[1:], data)
                    ]
                )
            )
            self.cursor.execute(query, (int(self.tbl.item(self.tbl.currentRow(), 0).text()),))
            self.connection.commit()
        self.draw_table()

    def delete_rec(self):
        row_num = self.tbl.currentRow()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"Удалить строку с id = {row_num}?")
        msg.setWindowTitle("Внимание!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        rc = msg.exec()
        if rc == QMessageBox.Ok:
            self.cursor.execute(DEL_QUERY, (int(self.tbl.item(self.tbl.currentRow(), 0).text()),))
            self.connection.commit()
            self.draw_table()

    def draw_table(self):
        self.tbl.setColumnCount(len(self.field_names))
        self.tbl.setRowCount(0)
        res = self.cursor.execute(GET_QUERY).fetchall()
        for i, row in enumerate(res):
            self.tbl.setRowCount(self.tbl.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tbl.setItem(i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Coffee()
    c.draw_table()
    c.show()
    sys.exit(app.exec())
