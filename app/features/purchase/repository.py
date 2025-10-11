# Melchizideck S. Osorno
class PurchaseRepository:
    def __init__(self, conn):
        self.conn = conn
        # Create sales table - matching transactions schema exactly
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def add_sale(self, receipt_number: str, item_name: str, price: float, quantity: int, total: float):
        """Add a sale record to purchase_data.db"""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO sales (receipt_number, item_name, price, quantity, total) VALUES (?, ?, ?, ?, ?)",
            (receipt_number, item_name, price, quantity, total),
        )
        self.conn.commit()
        return cur.lastrowid

    def list_sales(self):
        """List all sales from purchase_data.db"""
        rows = self.conn.execute(
            "SELECT id, receipt_number, item_name, price, quantity, total, date FROM sales ORDER BY id DESC"
        ).fetchall()
        return rows