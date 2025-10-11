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
    QLabel,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from app.core.db import purchase_get_conn
from .repository import PurchaseRepository
from .service import PurchaseService

class PurchaseView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("PurchaseView")

        # --- Wiring: core -> repo -> service ---
        self.service = PurchaseService(PurchaseRepository(purchase_get_conn()))

        # --- UI setup ---
        root = QVBoxLayout(self)

        form = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Product Name")

        self.quan = QSpinBox()
        self.quan.setRange(1, 10_000)
        self.quan.setValue(1)

        self.btn_add = QPushButton("Purchase")
        self.btn_clear = QPushButton("Clear")

        form.addWidget(QLabel("Name:"))
        form.addWidget(self.name)
        form.addWidget(QLabel("Quantity:"))
        form.addWidget(self.quan)
        form.addWidget(self.btn_add)
        form.addWidget(self.btn_clear)
        root.addLayout(form)

        # title
        title = QLabel("Purchase")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # Table: list all items from app_data.db
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Note"])
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        # Refresh Button
        actions = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setFixedWidth(250)
        self.btn_refresh.setStyleSheet("""
                    QPushButton {
                        padding: 10px;
                        font-size: 14px;
                        background-color: #BF00FF;
                        color: white;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #B57EDC;
                    }
                """)
        actions.addWidget(self.btn_refresh)
        actions.addStretch()
        root.addLayout(actions)

        # --- Signals ---
        self.btn_add.clicked.connect(self.on_purchase)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_refresh.clicked.connect(self.refresh)
        self.table.cellClicked.connect(self.on_cell_clicked)

        # Initial load
        self.refresh()

    def on_purchase(self):
        try:
            name = self.name.text().strip()
            quantity = int(self.quan.value())

            if not name:
                QMessageBox.warning(self, "Error", "Enter product name")
                return
            if quantity <= 0:
                QMessageBox.warning(self, "Error", "Enter valid quantity")
                return

            # Process purchase (deducts stock + saves to sales)
            sale = self.service.process_purchase(name, quantity)

            QMessageBox.information(
                self,
                "Success",
                f"Purchased {quantity} x {name}\nTotal: ₱{sale.total:,.2f}",
            )

            self.clear_form()
            self.refresh()
            self.refresh_other_views()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def refresh_other_views(self):
        """Refresh Dashboard and Transactions views if they exist"""
        try:
            # Find parent window and refresh other views
            main_window = self.window()
            if hasattr(main_window, 'features'):
                # Refresh Dashboard
                if 'Dashboard' in main_window.features:
                    dashboard = main_window.features['Dashboard']
                    if hasattr(dashboard, 'refresh'):
                        dashboard.refresh()

                # Refresh Transactions
                if 'Transactions' in main_window.features:
                    transactions = main_window.features['Transactions']
                    if hasattr(transactions, 'refresh'):
                        transactions.refresh()
        except Exception:
            pass  # Not fatal if refresh fails

    def clear_form(self):
        self.name.clear()
        self.quan.setValue(1)
        self.name.setStyleSheet("")

    def on_cell_clicked(self, row, _col):
        """Auto-fill product name when user double-clicks an item."""
        self.name.setText(self.table.item(row, 1).text())
        self.quan.setValue(1)

    def refresh(self):
        """Load all items from app_data.db."""
        items = self.service.list()
        self.table.setRowCount(len(items))
        for r, it in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(it.id)))
            self.table.setItem(r, 1, QTableWidgetItem(it.name))
            self.table.setItem(r, 2, QTableWidgetItem(it.price_display))
            self.table.setItem(r, 3, QTableWidgetItem(str(it.stock)))
            self.table.setItem(r, 4, QTableWidgetItem(it.note or ""))