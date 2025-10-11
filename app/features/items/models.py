# Melchizideck S. Osorno
from dataclasses import dataclass

@dataclass
class Item:
    id: int | None
    name: str
    price_cents: int  # Changed from 'price' to match database
    stock: int
    note: str = ""

    @property
    def price_display(self) -> str:
        return f"₱{self.price_cents/100:,.2f}"