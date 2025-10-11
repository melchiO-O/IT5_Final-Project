# Melchizideck S. Osorno
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime
from app.core.db import purchase_get_conn

def build_dashboard_view() -> QWidget:
    return DashboardView()

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardView")

        # --- UI ---
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        root.addWidget(title)

        # Analytics Cards Container
        cards_container = QHBoxLayout()
        cards_container.setSpacing(20)

        # Date & Time Card
        self.datetime_card = self.build_card("📅 Date & Time", "")
        cards_container.addWidget(self.datetime_card)

        # Total Sales Card
        self.sales_card = self.build_card("💰 Total Sales", "₱0.00")
        cards_container.addWidget(self.sales_card)

        # Total Transactions Card
        self.transactions_card = self.build_card("📊 Total Transactions", "0")
        cards_container.addWidget(self.transactions_card)

        root.addLayout(cards_container)

        # Refresh Button
        refresh_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Refresh Dashboard")
        self.btn_refresh.setFixedWidth(200)
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
        refresh_layout.addWidget(self.btn_refresh)
        refresh_layout.addStretch()
        root.addLayout(refresh_layout)

        root.addStretch()

        # Signals
        self.btn_refresh.clicked.connect(self.refresh)

        # Auto-update time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)

        # Initial refresh
        self.refresh()

    def build_card(self, title: str, value: str) -> QFrame:
        """Build a stat card widget"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(card)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #7f8c8d; font-weight: bold;")
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(value_label)

        return card

    def update_datetime(self):
        """Update the date & time display"""
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        datetime_label = self.datetime_card.findChild(QLabel, "value")
        if datetime_label:
            datetime_label.setText(f"{date_str}\n{time_str}")
            datetime_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")

    def calculate_total_sales(self) -> float:
        """Calculate total sales from purchase_data.db"""
        try:
            conn = purchase_get_conn()
            cursor = conn.cursor()
            result = cursor.execute("SELECT SUM(total) FROM sales").fetchone()
            return result[0] if result[0] else 0.0
        except Exception:
            return 0.0

    def calculate_total_transactions(self) -> int:
        """Calculate total number of transactions"""
        try:
            conn = purchase_get_conn()
            cursor = conn.cursor()
            result = cursor.execute("SELECT COUNT(*) FROM sales").fetchone()
            return result[0] if result[0] else 0
        except Exception:
            return 0

    def refresh(self):
        """Refresh all dashboard metrics"""
        # Update Total Sales
        total_sales = self.calculate_total_sales()
        sales_label = self.sales_card.findChild(QLabel, "value")
        if sales_label:
            sales_label.setText(f"₱{total_sales:,.2f}")

        # Update Total Transactions
        total_transactions = self.calculate_total_transactions()
        transactions_label = self.transactions_card.findChild(QLabel, "value")
        if transactions_label:
            transactions_label.setText(str(total_transactions))

        # Update DateTime
        self.update_datetime()