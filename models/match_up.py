from utils.manager import Manager
from uuid import UUID, uuid4
from typing import Union


class MatchUp:
    """
    Class representing a Match up

    Attributes:
    - Identifier : UUID or str
    - Players : list of players represented as dict {name : str, rank : int between 1000 and 3000, score: int}
    - Nb_round : int between 0 and 4
    """
    def __init__(self, identifier: Union[str, UUID], players: list, nb_round: int = 0):
        self.players = sorted(players, key=lambda x: x['rank'], reverse=True)
        for player in self.players:
            if not player.get("score"):
                player['score'] = 0
        err = []
        if len(self.players) < 8:
            err.append("Not enough players (min 8)")
        if len(self.players) % 2 != 0:
            err.append("Number of players must be pair")
        if err:
            raise AttributeError(err)
        self.identifier = identifier
        self.nb_round = nb_round
        self.matches = []

    def __repr__(self):
        return f"Match_up(" \
               f"players = {self.players}," \
               f"nb_round = {self.nb_round})"

    def __str__(self):
        return f"Match_up(" \
               f"Players: {self.players}\n" \
               f"Nb_round: {self.nb_round})"

    def __dict__(self):
        return {"players": self.players,
                "nb_round": self.nb_round,
                "identifier": str(self.identifier)}

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value: Union[str, UUID]):
        if not value:
            value = uuid4()
        if isinstance(value, str):
            try:
                value = UUID(value)
            except ValueError:
                raise AttributeError("Value is not uuid")
        if isinstance(value, UUID):
            if not value.version == 4:
                raise AttributeError("uuid must be in version 4.")
            else:
                self._identifier = value
        else:
            raise AttributeError("Value is not str")

    @staticmethod
    def name_match_up(p1, p2):
        return f"{min(p1['name'],p2['name'])} - {max(p1['name'],p2['name'])}"

    def check_match_up(self, name):
        return name in self.matches

    def create_match_up(self, p1, p2):
        name = self.name_match_up(p1, p2)
        if self.check_match_up(name):
            return False
        self.matches.append(name)
        return True

    def create_round(self):
        self.nb_round += 1
        if self.nb_round == 1:
            players = self.players
            self.create_match_up(players[0], players[4])
            self.create_match_up(players[1], players[5])
            self.create_match_up(players[2], players[6])
            self.create_match_up(players[3], players[7])
        else:
            players = sorted(self.players, key=lambda x: x['score'], reverse=True)
            while players:
                p1 = players.pop(0)
                for p2 in players:
                    if self.create_match_up(p1, p2):
                        players.pop(players.index(p2))
                        break
                else:
                    p2 = players.pop(0)
                    name = self.name_match_up(p1, p2)
                    self.matches.append(name)


mm = Manager(MatchUp, "match_up")
