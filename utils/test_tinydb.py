from tinydb import TinyDB
from models.p2 import Player


db = TinyDB('db.json')
players = db.table('players')


class ManagerTest:

    def __init__(self, filename: str):
        self.filename = filename
        self.db = TinyDB(filename, indent=4, sort_keys=True)
        self.players = self.db.table('players')
        self.tournaments = self.db.table('tournaments')

    def find_all(self):
        if self.filename == 'db.json':
            table = db.table('players')
        else:
            table = db.table('tournaments')
        return list(table.all())

    def create(self, *args, **kwargs):
        self.db.insert(*args, **kwargs)


if __name__ == '__main__':
    pm = ManagerTest('db.json')
    player = {"name": "Magnus", "rank": 2847}
    pm.create(player)
    print(pm.find_all())
