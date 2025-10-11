# Melchizideck S. Osorno
from .models import Sale
import random


class SaleRepository:
    def __init__(self, conn):
        self.conn = conn
        # Create sales table with receipt_number column
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

    def list(self) -> list[Sale]:
        res: list[Sale] = []
        rows = self.conn.execute(
            "SELECT id, receipt_number, item_name, price, quantity, total, date FROM sales ORDER BY id DESC"
        ).fetchall()

        if not rows:
            return []

        for r in rows:
            # Create Sale object with stored receipt_number
            sale = Sale(
                id=r[0],
                item_name=r[2],
                price=r[3],
                quantity=r[4],
                total=r[5]
            )
            # Override the random receipt_number with stored one
            sale._receipt_number = r[1]
            res.append(sale)

        return res

    def get(self, id_: int):
        """Get a single sale by ID including date and receipt_number"""
        row = self.conn.execute(
            "SELECT id, receipt_number, item_name, price, quantity, total, date FROM sales WHERE id=?",
            (id_,),
        ).fetchone()
        if row:
            return {
                'id': row[0],
                'receipt_number': row[1],
                'item_name': row[2],
                'price': row[3],
                'quantity': row[4],
                'total': row[5],
                'date': row[6]
            }
        return None

    def add(self, it: Sale) -> Sale:
        # Generate a permanent receipt number
        receipt_number = f"R{random.randint(10000, 99999)}"

        cur = self.conn.execute("""
            INSERT INTO sales (receipt_number, item_name, price, quantity, total)
            VALUES (?, ?, ?, ?, ?)
        """, (receipt_number, it.item_name, it.price, it.quantity, it.total))
        self.conn.commit()

        sale = Sale(
            id=cur.lastrowid,
            item_name=it.item_name,
            price=it.price,
            quantity=it.quantity,
            total=it.total
        )
        # Store the receipt number
        sale._receipt_number = receipt_number
        return sale