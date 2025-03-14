from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
import sys
from qt_material import apply_stylesheet


class ModernDataEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Data Entry Form")
        self.setGeometry(100, 100, 800, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form 1
        form1_layout = QHBoxLayout()

        self.warehouse_dropdown = QComboBox()
        self.warehouse_dropdown.addItems(["Warehouse A", "Warehouse B", "Warehouse C"])

        self.date_field = QDateEdit()
        self.date_field.setDate(QDate.currentDate())
        self.date_field.setCalendarPopup(True)

        self.ref_number_field = QLineEdit()

        form1_layout.addWidget(QLabel("Warehouse:"))
        form1_layout.addWidget(self.warehouse_dropdown)
        form1_layout.addWidget(QLabel("Date:"))
        form1_layout.addWidget(self.date_field)
        form1_layout.addWidget(QLabel("Reference Number:"))
        form1_layout.addWidget(self.ref_number_field)

        layout.addLayout(form1_layout)

        # Table (Form 2 inside table)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Reference Number", "Raw Material", "Status", "Qty", "Date", "Created by"])

        # Add Row (Inline Form in Table)
        self.add_inline_form()

        layout.addWidget(self.table)

        # Add button
        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self.add_record)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_inline_form(self):
        self.ref_number_input = QLineEdit()
        self.raw_material_input = QLineEdit()
        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["Pending", "Approved", "Rejected"])
        self.qty_input = QLineEdit()
        self.date_display = QLabel(QDate.currentDate().toString(Qt.DateFormat.ISODate))
        self.created_by_display = QLabel("Admin")

        # Connect Enter key press to add_record method
        self.ref_number_input.returnPressed.connect(self.add_record)
        self.raw_material_input.returnPressed.connect(self.add_record)
        self.qty_input.returnPressed.connect(self.add_record)

        self.table.insertRow(0)
        self.table.setCellWidget(0, 0, self.ref_number_input)
        self.table.setCellWidget(0, 1, self.raw_material_input)
        self.table.setCellWidget(0, 2, self.status_dropdown)
        self.table.setCellWidget(0, 3, self.qty_input)
        self.table.setCellWidget(0, 4, self.date_display)
        self.table.setCellWidget(0, 5, self.created_by_display)

    def add_record(self):
        ref_number = self.ref_number_input.text()
        raw_material = self.raw_material_input.text()
        status = self.status_dropdown.currentText()
        qty = self.qty_input.text()
        date = QDate.currentDate().toString(Qt.DateFormat.ISODate)
        created_by = "Admin"

        if ref_number and raw_material and qty:
            self.table.insertRow(1)  # Insert below inline form (at the top)
            self.table.setItem(1, 0, QTableWidgetItem(ref_number))
            self.table.setItem(1, 1, QTableWidgetItem(raw_material))
            self.table.setItem(1, 2, QTableWidgetItem(status))
            self.table.setItem(1, 3, QTableWidgetItem(qty))
            self.table.setItem(1, 4, QTableWidgetItem(date))
            self.table.setItem(1, 5, QTableWidgetItem(created_by))

            # Reset inline form
            self.ref_number_input.clear()
            self.raw_material_input.clear()
            self.qty_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_teal.xml')  # Apply modern theme
    window = ModernDataEntryForm()
    window.show()
    sys.exit(app.exec())
