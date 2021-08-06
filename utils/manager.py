import json
from typing import Union, Callable
from uuid import UUID


class Manager:

    def __init__(self, item_type: type, filename: str):
        self.filename = filename
        self.item_type = item_type
        self.items = {}
        self.load_from_json()

    def create(self, *args, **kwargs):
        item = self.item_type(*args, **kwargs)
        self.items[item.identifier] = item
        return item

    def load_from_json(self):
        with open(self.filename) as f:
            for item_data in json.load(f):
                self.create(**item_data)

    def find_all(self):
        return list(self.items.values())

    def find(self, identifier: Union[str, UUID]):
        if isinstance(identifier, str):
            try:
                identifier = UUID(identifier)
            except ValueError:
                raise AttributeError("Value is not uuid")
        return self.items[identifier]

    def find_by_criteria(self, key: Callable[[any], bool]):
        return [item for item in self.find_all() if key(item)]
