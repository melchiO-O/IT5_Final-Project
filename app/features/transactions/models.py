# Melchizideck S. Osorno
import random
from dataclasses import dataclass, field

@dataclass
class Sale:
    id: int | None
    item_name: str
    price: int
    quantity: int
    total: float
    _receipt_number: str = field(default=None, init=False)

    @property
    def price_display(self) -> str:
        return f"₱{self.price:,.2f}"

    @property
    def total_display(self) -> str:
        return f"₱{self.total:,.2f}"

    @property
    def receipt_number(self) -> str:
        """Return stored receipt number or generate a temporary one"""
        if self._receipt_number:
            return self._receipt_number
        # This should only be used as fallback
        return f"R{random.randint(10000, 99999)}"