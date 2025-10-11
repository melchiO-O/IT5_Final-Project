# Melchizideck S. Osorno
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel, QMessageBox,
)
from PyQt6.QtCore import Qt
from app.core.db import get_conn
from .repository import ItemRepository
from .service import ItemService
from .models import Item

def build_items_view() -> QWidget:
    return ItemsView()

class ItemsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ItemsView")

        # wiring: core -> repo -> service
        self.service = ItemService(ItemRepository(get_conn()))

        # --- UI ---
        root = QVBoxLayout(self)

        form = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Item name")
        self.price = QLineEdit()
        self.price.setPlaceholderText("Price (₱)")
        self.stock = QSpinBox()
        self.stock.setRange(0, 10_000)
        self.note = QLineEdit()
        self.note.setPlaceholderText("Note (optional)")
        self.btn_add = QPushButton("Add / Save")
        self.btn_clear = QPushButton("Clear")
        form.addWidget(QLabel("Name:"))
        form.addWidget(self.name)
        form.addWidget(QLabel("Price:"))
        form.addWidget(self.price)
        form.addWidget(QLabel("Stock:"))
        form.addWidget(self.stock)
        form.addWidget(self.note, 1)
        form.addWidget(self.btn_add)
        form.addWidget(self.btn_clear)
        root.addLayout(form)

        #title
        title = QLabel("Items")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Note"])
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        actions = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_delete = QPushButton("Delete Selected")
        actions.addWidget(self.btn_refresh)
        actions.addWidget(self.btn_delete)
        root.addLayout(actions)

        # state for editing
        self._editing_id: int | None = None

        # signals
        self.btn_add.clicked.connect(self.on_save)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.on_delete)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.refresh()

    def on_save(self):
        try:
            name = self.name.text().strip()
            pesos = float(self.price.text() or 0)
            price_cents = int(round(pesos * 100))
            stock = int(self.stock.value())
            note = self.note.text().strip()

            if self._editing_id is None:
                # Create
                self.service.create(name, price_cents, stock, note)
            else:
                # Update
                it = Item(
                    id=self._editing_id,
                    name=name,
                    price_cents=price_cents,
                    stock=stock,
                    note=note,
                )
                self.service.update(it)

            self.clear_form()
            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "Input Error", f"Error: {e}")
            # self.note.setStyleSheet("QLineEdit { border: 1px solid #d33; }")

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an item to delete.")
            return

        id_ = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()

        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{name}' (ID: {id_})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return  # user cancelled

        # Proceed with deletion
        try:
            self.service.delete(id_)
            if self._editing_id == id_:
                self.clear_form()
            QMessageBox.information(self, "Deleted", f"Item '{name}' was deleted successfully.")

            self.refresh()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete item: {e}")

    def on_cell_double_clicked(self, row, _col):
        # Load row into form for editingv
        self._editing_id = int(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        price_text = self.table.item(row, 2).text().replace("₱", "").replace(",", "")
        self.price.setText(price_text)
        self.stock.setValue(int(self.table.item(row, 3).text()))
        self.note.setText(self.table.item(row, 4).text())
        self.btn_add.setText("Save Changes")

    def clear_form(self):
        self._editing_id = None
        self.name.clear()
        self.price.clear()
        self.note.clear()
        self.stock.setValue(0)
        self.btn_add.setText("Add / Save")
        self.note.setStyleSheet("")
        self.note.setPlaceholderText("Note (optional)")

    def refresh(self):
        items = self.service.list()
        self.table.setRowCount(len(items))
        for r, it in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(it.id)))
            self.table.setItem(r, 1, QTableWidgetItem(it.name))
            self.table.setItem(r, 2, QTableWidgetItem(it.price_display))
            self.table.setItem(r, 3, QTableWidgetItem(str(it.stock)))
            self.table.setItem(r, 4, QTableWidgetItem(it.note))
            #self.table.resizeColumnsToContents()
