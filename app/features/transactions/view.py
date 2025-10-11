# Melchizideck S. Osorno
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from app.core.db import purchase_get_conn
from .repository import SaleRepository
from .service import SaleService
from .receipt import ReceiptDialog

class SalesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("SalesView")
        # Connect to purchase_data.db where sales are stored
        self.service = SaleService(SaleRepository(purchase_get_conn()))

        root = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Transaction History")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()

        root.addLayout(header)

        # Info label
        info_label = QLabel("Click on any row to view receipt")
        info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
                font-style: italic;
                padding: 5px;
                background-color: #ecf0f1;
                border-radius: 3px;
            }
        """)
        root.addWidget(info_label)

        # Sales table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Receipt #", "Item Name", "Price", "Quantity", "Total"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setStyleSheet("""
            QTableWidget {
                selection-background-color: #3498db;
            }
            QTableWidget::item:hover {
                background-color: #ecf0f1;
                cursor: pointer;
            }
        """)
        root.addWidget(self.table)

        # Actions
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

        # Store sale items for easy access
        self.sale_items = []

        # Signals
        self.btn_refresh.clicked.connect(self.refresh)
        self.table.cellClicked.connect(self.show_receipt)

        # Load data initially
        self.refresh()

    def show_receipt(self, row, column=None):
        """Show receipt dialog for the selected transaction"""
        if row < 0 or row >= len(self.sale_items):
            return

        # Get the sale item
        sale = self.sale_items[row]

        # Prepare sale data for receipt using stored receipt_number
        sale_data = {
            'id': sale.id,
            'receipt_number': sale.receipt_number,  # Uses stored receipt_number
            'item_name': sale.item_name,
            'price': sale.price,
            'quantity': sale.quantity,
            'total': sale.total,
        }

        # Show receipt dialog
        dialog = ReceiptDialog(sale_data, self)
        dialog.exec()

    def refresh(self):
        """Refresh the transactions table"""
        self.table.setRowCount(0)
        self.sale_items = self.service.list()

        # Populate table
        self.table.setRowCount(len(self.sale_items))
        for r, it in enumerate(self.sale_items):
            # Receipt Number - uses stored receipt_number
            receipt_item = QTableWidgetItem(str(it.receipt_number))
            receipt_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, 0, receipt_item)

            # Item Name
            self.table.setItem(r, 1, QTableWidgetItem(it.item_name))

            # Price
            price_item = QTableWidgetItem(it.price_display)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 2, price_item)

            # Quantity
            qty_item = QTableWidgetItem(str(it.quantity))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, 3, qty_item)

            # Total
            total_item = QTableWidgetItem(it.total_display)
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(r, 4, total_item)