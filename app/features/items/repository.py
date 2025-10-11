# Melchizideck S. Osorno
from .models import Item

class ItemRepository:
    def __init__(self, conn):
        self.conn = conn
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price_cents INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        note TEXT DEFAULT ''
        )
        """
        )

    def list(self) -> list[Item]:
        res: list[Item] = []
        rows = self.conn.execute(
            "SELECT id, name, price_cents, stock, note FROM items ORDER BY id DESC"
        ).fetchall()

        if not rows:
            return []

        for r in rows:
            item = Item(*r)
            res.append(item)

        return res

    def get(self, id_: int) -> Item | None:
        row = self.conn.execute(
            "SELECT id, name, price_cents, stock, note FROM items WHERE id=?",
            (id_,),
        ).fetchone()
        return Item(*row) if row else None

    def add(self, it: Item) -> Item:
        cur = self.conn.execute(
            "INSERT INTO items(name,price_cents,stock,note) VALUES (?,?,?,?)",
            (it.name, it.price_cents, it.stock, it.note),
        )
        self.conn.commit()
        return Item(
            id=cur.lastrowid,
            name=it.name,
            price_cents=it.price_cents,
            stock=it.stock,
            note=it.note,
        )

    def update(self, it: Item) -> Item:
        assert it.id is not None
        self.conn.execute(
            "UPDATE items SET name=?, price_cents=?, stock=?, note=? WHERE id=?",
            (it.name, it.price_cents, it.stock, it.note, it.id),
        )
        self.conn.commit()
        return it

    def delete(self, id_: int) -> None:
        self.conn.execute("DELETE FROM items WHERE id=?", (id_,))
        self.conn.commit()