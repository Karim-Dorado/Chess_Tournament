from utils.router import router
from utils.menu import Menu
from utils.form import Form
from utils.checkers import check_rank, check_tournaments, check_match_up, check_round, check_winner, check_player
from models.player import pm
from models.tournament import tm
from models.match_up import mm


def main():
    path = Menu('Main Menu', [("Players Menu", '/players'),
                              ('Tournaments Menu', '/tournaments'),
                              ("Quit", '/quit')]).show()
    router.navigate(path)


def players():
    path = Menu('Players Menu', [("Create a new player", '/players/create'),
                                 ("Change a player rank", '/players/update'),
                                 ("Players list", '/players/list'),
                                 ("Return to Main Menu", '/'),
                                 ("Quit", '/quit')]).show()
    router.navigate(path)


def tournaments():
    path = Menu('Tournament Menu', [("Create a new tournament", '/tournaments/create'),
                                    ("Tournaments list", '/tournaments/list'),
                                    ("Start a tournament", '/tournaments/start'),
                                    ("Back to Main Menu", '/'),
                                    ("Quit", '/quit')]).show()
    router.navigate(path)


def create_player():
    data = Form("Create a new player", [("First name", "first_name"),
                                        ('Last name', "last_name"),
                                        ("Birthdate", "birthdate"),
                                        ("Gender", "gender"),
                                        ("Rank", "rank")]).show()
    pm.create(**data)
    pm.insert(**data)
    router.navigate("/players")


def create_tournament():
    if len(pm.find_all()) < 8:
        print("Not enough players registered in database")
    else:
        data = Form("Create a new tournament", [('Tournament name', "name"),
                                                ('Place', 'place'),
                                                ("Start date", "start_date"),
                                                ("End date", "end_date"),
                                                ("Time control", "time_control"),
                                                ("Players", "players"),
                                                ("Description", "description")]).show()
        tm.create(**data)
        tm.insert(**data)
    router.navigate("/tournaments")


def list_players():
    path = Menu('Players list', [("Sorted by name", '/players/list/by_name'),
                                 ("Sorted by rank ", '/players/list/by_rank'),
                                 ("Back to Player Menu", '/players'),
                                 ("Quit", '/quit')]).show()

    players_list = pm.find_all()
    if path == '/players/list/by_name':
        for player in sorted(players_list, key=lambda x: (x.last_name, x.first_name, -x.rank)):
            print(player)
    elif path == '/players/list/by_rank':
        for player in sorted(players_list, key=lambda x: (-x.rank, x.last_name, x.first_name)):
            print(player)
    else:
        router.navigate(path)
    router.navigate("/players")


def list_tournaments():
    for tournament in tm.find_all():
        print(tournament)
    router.navigate("/tournaments")


def update_player_rank():
    player_identifier = check_player()
    player = pm.find(player_identifier)
    new_rank = check_rank()
    player.rank = new_rank
    pm.update(**player.__dict__())
    router.navigate("/players")


def update_player_rank1():
    players = pm.find_all()
    identifier = input("Enter player identifier: ")
    for player in players:
        if str(player.identifier) == identifier:
            new_rank = check_rank()
            player.rank = new_rank
    router.navigate("/players")


def start_tournament():
    tournament_identifier = check_tournaments()
    match_up = check_match_up(tournament_identifier)
    check = True
    while check:
        if match_up.nb_round < 4:
            matches = check_round(match_up)
            for match in matches:
                check_winner(match[0], match[1])
            check = Menu("Continue tournament ?", [("Yes", True), ("No", False)]).show()
        else:
            print("Tournament Finished")
            check = False
    mm.update(**match_up.__dict__())
    router.navigate("/tournaments")
