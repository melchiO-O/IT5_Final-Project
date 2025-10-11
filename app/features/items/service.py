# Melchizideck S. Osorno
from .models import Item
from .repository import ItemRepository


class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    # Basic business rules
    def validate(self, it: Item):
        if not it.name.strip():
            raise ValueError("Name is required")
        if it.price_cents < 0:
            raise ValueError("Price must be >= 0")
        if it.stock < 0:
            raise ValueError("Stock must be >= 0")

    # CRUD
    def list(self):
        return self.repo.list()

    def create(self, name: str, price_cents: int, stock: int, note: str = "") -> Item:
        it = Item(id=None, name=name, price_cents=price_cents, stock=stock, note=note)
        self.validate(it)
        return self.repo.add(it)

    def update(self, it: Item) -> Item:
        self.validate(it)
        return self.repo.update(it)

    def delete(self, id_: int) -> None:
        self.repo.delete(id_)
