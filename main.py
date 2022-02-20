import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


QUERY = """SELECT *
    FROM CoffeeKinds
    ORDER BY CoffeeKinds.id"""


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        cursor = self.connection.cursor()
        res = cursor.execute(QUERY).fetchall()
        field_names = [f[0] for f in cursor.description]
        self.tbl.setColumnCount(7)
        self.tbl.setRowCount(0)
        for i, row in enumerate(res):
            self.tbl.setRowCount(self.tbl.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tbl.setItem(i, j, QTableWidgetItem(str(elem)))
        for i in range(7):
            title = QTableWidgetItem()  # <---
            title.setText(field_names[i])  # <---
            self.tbl.setHorizontalHeaderItem(i, title)

    def closeEvent(self, event):
        self.connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Coffee()
    c.show()
    sys.exit(app.exec())
