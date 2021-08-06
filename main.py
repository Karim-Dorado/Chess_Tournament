from utils.router import router
from utils.menu import Menu
from utils.form import Form
from utils.checkers import check_rank
from models.player import pm
from models.tournament import tm
from models.match_up import MatchUp


def main():
    path = Menu('Menu principal', [("Menu joueurs", '/players'),
                                   ('Menu tournois', '/tournaments'),
                                   ("Quitter", '/quit')]).show()
    router.navigate(path)


def players():
    path = Menu('Menu Joueurs', [("Créer un joueur", '/players/create'),
                                 ("Changer le rang d'un joueur", '/players/update'),
                                 ("Liste des joueurs", '/players/list'),
                                 ("Retour au menu principal", '/'),
                                 ("Quitter", '/quit')]).show()
    router.navigate(path)


def tournaments():
    path = Menu('Menu Tournois', [("Créer un tournois", '/tournaments/create'),
                                  ("Liste des tournois", '/tournaments/list'),
                                  ("Démarrer un tournois", '/tournaments/start'),
                                  ("Retour au menu principal", '/'),
                                  ("Quitter", '/quit')]).show()
    router.navigate(path)


def create_player():
    data = Form("Creation d'un joueur", [("Prénom", "first_name"),
                                         ('Nom', "last_name"),
                                         ("Date de naissance", "birthdate"),
                                         ("Genre", "gender"),
                                         ("Rang", "rank")]).show()
    pm.create(**data)
    router.navigate("/players")


def create_tournament():
    data = Form("Création d'un tournois", [('Nom', "name"),
                                           ('Place', 'place'),
                                           ("Début", "start_date"),
                                           ("Fin", "end_date"),
                                           ("Control", "time_control"),
                                           ("Joueurs", "players"),
                                           ("Description", "description")]).show()
    tm.create(**data)
    router.navigate("/tournaments")


def list_players():
    path = Menu('Liste des joueurs', [("Triés par nom", '/players/list/by_name'),
                                      ("Triés par rang ", '/players/list/by_rank'),
                                      ("Retour au menu joueur", '/players'),
                                      ("Quitter", '/quit')]).show()

    if path == '/players/list/by_name':
        for player in sorted(pm.find_all(), key=lambda x: (x.last_name, x.first_name, -x.rank)):
            print(f'NAME: {player.last_name} {player.first_name}\n'
                  f'RANK : {player.rank}\n'
                  f'ID: {player.identifier}\n')
        router.navigate("/players")
    elif path == '/players/list/by_rank':
        for player in sorted(pm.find_all(), key=lambda x: (-x.rank, x.last_name, x.first_name)):
            print(f'NAME: {player.last_name} {player.first_name}\n'
                  f'RANK : {player.rank}\n'
                  f'ID: {player.identifier}\n')
        router.navigate("/players")
    else:
        router.navigate(path)


def list_tournaments():
    for tournament in tm.find_all():
        if tournament.start_date == tournament.end_date:
            print(f'NAME: {tournament.name}\n'
                  f'PLACE: {tournament.place}\n'
                  f'DATE: {tournament.start_date}\n'
                  f'TIME CONTROL: {tournament.time_control}\n'
                  f'ID: {tournament.identifier}\n')
        else:
            print(f'NAME: {tournament.name}\n'
                  f'PLACE: {tournament.place}\n'
                  f'DATE: from {tournament.start_date} to {tournament.end_date}\n'
                  f'TIME CONTROL: {tournament.time_control}\n'
                  f'ID: {tournament.identifier}\n')
    router.navigate("/tournaments")


def update_player_rank():
    players = pm.find_all()
    identifier = input("Enter player identifier: ")
    for player in players:
        if str(player.identifier) == identifier:
            new_rank = check_rank()
            player.rank = new_rank
    router.navigate("/players")

def start_tounament():
    tournaments = tm.find_all()
    identifier = input("Enter tournament identifier: ")
    for tournament in tournaments:
        if str(tournament.identifier) == identifier:
            players = []
            for player in tournament.players:
                players.append({'name': player.last_name + " " + player.first_name, "rank": player.rank})
            match_up = MatchUp(*players)
            for i in range(1, 4):
                match_up.create_round2()
                print(match_up.matches[-4:])
                print(f"--- ROUND {i} ---")
                if i == 1:
                    sorted(players, key=lambda x: x['rank'], reverse=True)
                    matches = (players[0], players[4]), \
                              (players[1], players[5]), \
                              (players[2], players[6]), \
                              (players[3], players[7])
                else:
                    p = sorted(players, key=lambda x: x['score'], reverse=True)
                    matches = (p[0], p[1]), \
                              (p[2], p[3]), \
                              (p[4], p[5]), \
                              (p[6], p[7])
                for match in matches:
                    winner = [match[0], match[1], None]
                    options = {}
                    check = True
                    for nb, player in enumerate(winner, start=1):
                        options[nb] = player
                    for key in options:
                        if options[key] is not None:
                            print(f"OPTION {key}: {options[key]['name']}")
                        else:
                            print(f"OPTION {key}: {options[key]}")
                    response = input("Choose a winner: ")
                    while check:
                        try:
                            if int(response) in options:
                                if int(response) == 1:
                                    winner[0]['score'] += 1
                                elif int(response) == 2:
                                    winner[1]['score'] += 1
                                elif int(response) == 3:
                                    winner[0]['score'] += 0.5
                                    winner[1]['score'] += 0.5
                                check = False
                            else:
                                raise ValueError
                        except (KeyError, ValueError):
                            print(f"Please enter a valid response (must be an integer)")
                            response = input(f"Choose a winner: ")
                    for player in players:
                        if player in winner:
                            print(player['name'], "Score:", player['score'])


if __name__ == '__main__':
    router.add_route("/", main)
    router.add_route("/players", players)
    router.add_route("/tournaments", tournaments)
    router.add_route("/players/create", create_player)
    router.add_route("/players/update", update_player_rank)
    router.add_route("/players/list", list_players)
    router.add_route("/tournaments/create", create_tournament)
    router.add_route("/tournaments/list", list_tournaments)
    router.add_route("/tournaments/start", start_tounament)
    router.add_route("/quit", quit)
    router.navigate("/")
