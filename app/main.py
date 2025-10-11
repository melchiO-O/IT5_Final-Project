# Melchizideck S. Osorno
import sys
from PyQt6.QtWidgets import QApplication

from app.features.dashboard.view import build_dashboard_view
from app.features.items.view import build_items_view
from app.features.purchase.view import PurchaseView
from app.features.transactions.view import SalesView
from app.shell.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Optional: load app stylesheet
    try:
        with open("app/core/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    # Create main window
    win = MainWindow()

    # Add features
    win.add_feature("Dashboard", build_dashboard_view)
    win.add_feature("Items", build_items_view)
    win.add_feature("Purchase", PurchaseView)
    win.add_feature("Transactions", SalesView)

    win.resize(1000, 600)
    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()