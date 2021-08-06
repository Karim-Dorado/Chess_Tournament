class MatchUp:
    """

    """
    def __init__(self, *players: dict):
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
        self.nb_round = 0
        self.matches = []

    def __repr__(self):
        return f"Matchup{self.players}"

    def __str__(self):
        return f"{self.players}"

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

    def create_round(self, *winner):
        self.nb_round += 1
        if self.nb_round == 1:
            players = self.players
            g1 = players[0:4]
            g2 = players[4:8]
            self.create_match_up(players[0], players[4])
            self.create_match_up(players[1], players[5])
            self.create_match_up(players[2], players[6])
            self.create_match_up(players[3], players[7])
            for i in range(4):
                if g1[i]['name'] in winner:
                    if g2[i]['name'] in winner:
                        raise AttributeError(f"{g1[i]['name']} and {g2[i]['name']} can't both be winners")
                    g1[i]['score'] += 1
                elif g2[i]['name'] in winner:
                    if g1[i]['name'] in winner:
                        raise AttributeError(f"{g1[i]['name']} and {g2[i]['name']} can't both be winners")
                    g2[i]['score'] += 1
                else:
                    g1[i]['score'] += 0.5
                    g2[i]['score'] += 0.5
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
                if p1['name'] in winner:
                    if p2['name'] in winner:
                        raise AttributeError(f"{p1['name']} and {p2['name']} can't both be winners")
                    p1['score'] += 1
                elif p2['name'] in winner:
                    if p1['name'] in winner:
                        raise AttributeError(f"{p1['name']} and {p2['name']} can't both be winners")
                    p2['score'] += 1
                else:
                    p1['score'] += 0.5
                    p2['score'] += 0.5

    def create_round2(self):
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


if __name__ == '__main__':
    a = {'name': "a", "rank": 2800}
    b = {'name': "b", "rank": 2600}
    c = {'name': "c", "rank": 2500}
    d = {'name': "d", "rank": 2400}
    e = {'name': "e", "rank": 2200}
    f = {'name': "f", "rank": 1500}
    g = {'name': "g", "rank": 1200}
    h = {'name': "h", "rank": 1000}
    m = MatchUp(a, b, d, c, e, f, g, h)
    m.create_round2()
    a['score'] = 1
    b['score'] = 1
    c['score'] = 1
    d['score'] = 1
    e['score'] = 0
    f['score'] = 0
    g['score'] = 0
    h['score'] = 0
    print(m.matches)
    print(m)
    m.create_round2()
    b['score'] += 1
    c['score'] += 1
    e['score'] += 1
    h['score'] += 1
    print(m.matches)
    print(m)
    m.create_round2()
    c['score'] += 1
    a['score'] += 1
    f['score'] += 1
    e['score'] += 1
    print(m.matches)
    print(m)
    m.create_round2()
    b['score'] += 1
    a['score'] += 1
    d['score'] += 1
    h['score'] += 1
    print(m.matches)
    print(m)
    print((m.matches[-4:]))
    """
    round1 = m.create_round()
    print(m.matches)
    print(m)
    round2 = m.create_round()
    print(m.matches)
    print(m)
    round3 = m.create_round()
    print(m.matches)
    print(m)
    round4 = m.create_round()
    print(m.matches)
    print(m)
    round5 = m.create_round()
    print(m.matches)
    print(m)
    round6 = m.create_round()
    print(m.matches)
    print(m)
    round7 = m.create_round()
    print(m.matches)
    print(m)

    round1 = m.create_round("a", "b", "c", "d")
    print(m.matches)
    print(m)
    round2 = m.create_round("b", "c", "e", "h")
    print(m.matches)
    print(m)
    round3 = m.create_round("c", "a", "f", "e")
    print(m.matches)
    print(m)
    round4 = m.create_round("b", "a", "d", "h")
    print(m.matches)
    print(m)
    
    round1 = m.create_round("a", "b", "c", "d")
    print(m.matches)
    print(m)
    round2 = m.create_round("a", "c", "e", "h")
    print(m.matches)
    print(m)
    round3 = m.create_round("b", "a", "f", "e")
    print(m.matches)
    print(m)
    round4 = m.create_round("b", "a", "e", "h")
    print(m.matches)
    print(m)
    """