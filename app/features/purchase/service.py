from .repository import PurchaseRepository
from app.features.items.repository import ItemRepository
from app.features.transactions.repository import SaleRepository
from app.features.transactions.models import Sale
from app.core.db import get_conn, purchase_get_conn
import random


class PurchaseService:
    def __init__(self, repo: PurchaseRepository):
        self.repo = repo

    def list(self):
        """Returns list of items from main database for display"""
        item_repo = ItemRepository(get_conn())
        return item_repo.list()

    def process_purchase(self, name: str, quantity: int):
        """Handles item lookup, stock deduction, and saving to transactions."""

        # Connect to the main items database and find item
        item_repo = ItemRepository(get_conn())
        items = item_repo.list()
        item = next((i for i in items if i.name.lower() == name.lower()), None)

        if not item:
            raise ValueError(f"Item '{name}' not found.")

        if item.stock < quantity:
            raise ValueError(f"Not enough stock for '{item.name}'. Available: {item.stock}")

        # Calculate totals
        price_in_pesos = item.price_cents / 100
        total = price_in_pesos * quantity

        # Generate permanent receipt number
        receipt_number = f"R{random.randint(10000, 99999)}"

        # Deduct stock from items database
        item.stock = item.stock - quantity
        item_repo.update(item)

        # Add to sales database (purchase_data.db)
        sale_repo = SaleRepository(purchase_get_conn())
        sale = Sale(
            id=None,
            item_name=item.name,
            price=price_in_pesos,
            quantity=quantity,
            total=total
        )
        # Add sale (this will generate and store receipt_number)
        saved_sale = sale_repo.add(sale)

        return saved_sale