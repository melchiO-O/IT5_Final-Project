# Melchizideck S. Osorno
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from app.core.db import purchase_get_conn

class ReceiptDialog(QDialog):
    def __init__(self, sale_data, parent=None):
        super().__init__(parent)
        self.sale_data = sale_data
        self.setWindowTitle("Receipt")
        self.setModal(True)
        self.setFixedSize(320, 480)

        # Fetch full transaction details including date
        self.fetch_transaction_date()

        self.setup_ui()

    def fetch_transaction_date(self):
        """Fetch the actual transaction date from database"""
        try:
            conn = purchase_get_conn()
            cursor = conn.cursor()
            result = cursor.execute(
                "SELECT date FROM sales WHERE id=?",
                (self.sale_data['id'],)
            ).fetchone()

            if result and result[0]:
                try:
                    self.transaction_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
                except:
                    self.transaction_date = datetime.now()
            else:
                self.transaction_date = datetime.now()
        except:
            self.transaction_date = datetime.now()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Receipt container
        receipt_container = QFrame()
        receipt_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px dashed #999;
            }
        """)

        receipt_layout = QVBoxLayout(receipt_container)
        receipt_layout.setContentsMargins(25, 25, 25, 25)
        receipt_layout.setSpacing(8)

        # Store Name
        store_name = QLabel("MHIE-ni MART")
        store_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        store_name.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        store_name.setStyleSheet("color: #4B0082;")
        receipt_layout.addWidget(store_name)

        # Dashed line
        receipt_layout.addWidget(self.create_dashed_line())
        receipt_layout.addSpacing(5)

        # Receipt number
        receipt_num = QLabel(f"Receipt #: {self.sale_data['receipt_number']}")
        receipt_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_num.setFont(QFont("Courier New", 8))
        receipt_num.setStyleSheet("color: #000000;")
        receipt_layout.addWidget(receipt_num)

        receipt_layout.addSpacing(5)

        # Date and Time
        date_time = QLabel(self.transaction_date.strftime("%m/%d/%Y %I:%M %p"))
        date_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_time.setFont(QFont("Courier New", 9))
        date_time.setStyleSheet("color: #000000;")
        receipt_layout.addWidget(date_time)

        receipt_layout.addSpacing(5)
        receipt_layout.addWidget(self.create_dashed_line())
        receipt_layout.addSpacing(10)


        # Items header
        items_layout = QVBoxLayout()
        items_layout.setSpacing(3)

        # Single item
        item_num = QLabel(f"1. {self.sale_data['item_name']}")
        item_num.setFont(QFont("Courier New", 9))
        item_num.setStyleSheet("color: #000;")
        items_layout.addWidget(item_num)

        # Price and quantity line
        price_qty_layout = QHBoxLayout()
        price_qty = QLabel(f"   ₱{self.sale_data['price']:.2f} x {self.sale_data['quantity']}")
        price_qty.setFont(QFont("Courier New", 9))
        price_qty.setStyleSheet("color: #555;")

        item_total = QLabel(f"₱{self.sale_data['total']:.2f}")
        item_total.setFont(QFont("Courier New", 9))
        item_total.setStyleSheet("color: #000;")
        item_total.setAlignment(Qt.AlignmentFlag.AlignRight)

        price_qty_layout.addWidget(price_qty)
        price_qty_layout.addWidget(item_total)
        items_layout.addLayout(price_qty_layout)

        receipt_layout.addLayout(items_layout)

        receipt_layout.addSpacing(10)
        receipt_layout.addWidget(self.create_dashed_line())
        receipt_layout.addSpacing(5)

        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("TOTAL")
        total_label.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        total_label.setStyleSheet("color: #000;")

        total_amount = QLabel(f"₱{self.sale_data['total']:.2f}")
        total_amount.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        total_amount.setStyleSheet("color: #000;")
        total_amount.setAlignment(Qt.AlignmentFlag.AlignRight)

        total_layout.addWidget(total_label)
        total_layout.addWidget(total_amount)
        receipt_layout.addLayout(total_layout)

        receipt_layout.addSpacing(10)
        receipt_layout.addWidget(self.create_dashed_line())
        receipt_layout.addSpacing(10)

        # Thank you
        thanks = QLabel("THANK YOU, MHIE!")
        thanks.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thanks.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        thanks.setStyleSheet("color: #000;")
        receipt_layout.addWidget(thanks)

        receipt_layout.addStretch()

        layout.addWidget(receipt_container)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 10, 15, 10)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def create_dashed_line(self) -> QLabel:
        """Create a dashed line separator"""
        line = QLabel("- - - - - - - - - - - - - - - - - - - - - - -")
        line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line.setFont(QFont("Courier New", 8))
        line.setStyleSheet("color: #999;")
        return line

    def add_amount_row(self, layout, label_text, amount):
        """Add an amount row (subtotal, discount, etc)"""
        row_layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setFont(QFont("Courier New", 9))
        label.setStyleSheet("color: #333;")

        value = QLabel(f"₱{amount:.2f}")
        value.setFont(QFont("Courier New", 9))
        value.setStyleSheet("color: #333;")
        value.setAlignment(Qt.AlignmentFlag.AlignRight)

        row_layout.addWidget(label)
        row_layout.addWidget(value)

        layout.addLayout(row_layout)