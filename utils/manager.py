from tinydb import TinyDB, Query
from typing import Union, Callable
from uuid import UUID


class Manager:
    """
    Class Manager that makes a link between models and database
    """
    def __init__(self, item_type: type, item_table: str):
        self.db = TinyDB('db.json', indent=4, sort_keys=True)
        self.item_type = item_type
        self.item_table = item_table
        self.items = {}
        self.load_from_json()

    def find_all(self):
        """Allows to find all items (players, tournament or match_up) stored in database and return them as a list"""
        return list(self.items.values())

    def create(self, *args, **kwargs):
        """Allows to create an item (players, tournament or match_up) from a dictionary"""
        item = self.item_type(*args, **kwargs)
        self.items[item.identifier] = item
        return item

    def insert(self, *args, **kwargs):
        """Allows to insert an item (players, tournament or match_up) in database"""
        item = self.item_type(*args, **kwargs)
        table = self.db.table(self.item_table)
        table.insert(item.__dict__())

    def update(self, *args, **kwargs):
        """Allows to update an item (players, tournament or match_up) from database"""
        User = Query()
        item = self.item_type(*args, **kwargs)
        table = self.db.table(self.item_table)
        table.update(item.__dict__(), User.identifier == str(item.identifier))

    def load_from_json(self):
        table = self.db.table(self.item_table)
        for item_data in table:
            self.create(**item_data)

    def find(self, identifier: Union[str, UUID]):
        """Allows to find an item stored in database"""
        if isinstance(identifier, str):
            try:
                identifier = UUID(identifier)
            except ValueError:
                raise AttributeError("Value is not uuid")
        return self.items[identifier]

    def find_by_criteria(self, key: Callable[[any], bool]):
        return [item for item in self.find_all() if key(item)]
