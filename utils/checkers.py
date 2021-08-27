import re
from datetime import date
from utils.constante import REGEX, GENDER, TIME_CONTROL
from models.player import pm
from models.tournament import tm
from models.match_up import MatchUp, mm
from utils.menu import Menu


def check_name(value: str):
    check = input(f"{value.capitalize()}: ")
    while not re.match(REGEX, check):
        print(f'invalid {value}')
        check = input(f"{value.capitalize()}: ")
    return check


def check_gender():
    gender = input("Gender (m/f): ")
    while not gender.upper() in GENDER:
        print("Please enter a valid gender (m/f)")
        gender = input("Gender (m/f): ")
    return gender


def check_date(value: list = None):
    check_b = True
    while check_b:
        check_y = True
        while check_y:
            year = input("Year: ")
            if year.isdigit():
                if len(year) == 4:
                    if not value:
                        check_y = False
                    else:
                        if value[0] <= int(year) <= value[1]:
                            check_y = False
                        else:
                            print(f"Year must be between {value[0]} and {value[1]}")
                else:
                    print("Maximum 4 digit")
            else:
                print("Year must be digit")
        check_m = True
        while check_m:
            month = input("Month (between 01 and 12): ")
            if month.isdigit():
                if 1 <= len(month) <= 2:
                    if 1 <= int(month) <= 12:
                        if len(month) == 1:
                            month = f'0{month}'
                        check_m = False
                    else:
                        print("Month must be between 01 and 12")
                else:
                    print("Maximum 2 digit")
            else:
                print("Month must be digit")
        check_d = True
        while check_d:
            day = input("Day (between 01 and 31): ")
            if day.isdigit():
                if 1 <= len(day) <= 2:
                    if 1 <= int(day) <= 31:
                        if len(day) == 1:
                            day = f'0{day}'
                        check_d = False
                    else:
                        print("Day must be between 01 and 31")
                else:
                    print("Maximum 2 digit")
            else:
                print("Day must be digit")
        try:
            date_iso_format = date.fromisoformat(f"{year}-{month}-{day}")
            check_b = False
        except ValueError:
            print("Day is out of range for month")
    return str(date_iso_format)


def check_rank():
    check = True
    while check:
        rank = input("Rank(between 1000 and 3000): ")
        if rank.isdigit():
            if 1000 <= int(rank) <= 3000:
                check = False
            else:
                print("Rank must be in range 1000 - 3000")
        else:
            print("Rank value must be digit")
    return int(rank)


def check_time_control():
    time_control = input("Time control: ")
    while not time_control.upper() in TIME_CONTROL:
        print("Please enter a valid time control (Bullet, Blitz or Rapid)")
        time_control = input("Time control: ")
    return time_control


def check_description():
    description = input("Description: ")
    while len(description) > 250:
        print("250 characters max")
        description = input("Description: ")
    return description


def check_player():
    players = pm.find_all()
    choices = []
    for player in players:
        choices.append((player.first_name + " " + player.last_name, str(player.identifier)))
    choice = Menu('Choose player', choices).show()
    return choice


def check_players():
    players = pm.find_all()
    choices = []
    players_list = []
    for player in players:
        choices.append((player.first_name + " " + player.last_name, str(player.identifier)))
    for i in range(8):
        for choice in choices:
            if choice[1] in players_list:
                choices.remove(choice)
        menu = Menu('Add players', choices).show()
        players_list.append(menu)
    return players_list


def check_tournaments():
    tournaments = tm.find_all()
    choices = []
    for tournament in tournaments:
        choices.append((tournament.name, str(tournament.identifier)))
    menu = Menu('Choose tournament', choices).show()
    return menu


def check_match_up(identifier: str):
    tournament = tm.find(identifier)
    try:
        match_up = mm.find(identifier)
    except KeyError:
        players = []
        for value in tournament.players:
            player = pm.find(value)
            players.append({'name': player.last_name + " " + player.first_name, "rank": player.rank})
        data = {"identifier": identifier, "players": players}
        match_up = mm.create(**data)
        mm.insert(**data)
    return match_up


def check_round(match_up: MatchUp):
    match_up.create_round()
    print(f"--- ROUND {match_up.nb_round} ---")
    if match_up.nb_round == 1:
        sorted(match_up.players, key=lambda x: x['rank'], reverse=True)
        matches = (match_up.players[0], match_up.players[4]), \
                  (match_up.players[1], match_up.players[5]), \
                  (match_up.players[2], match_up.players[6]), \
                  (match_up.players[3], match_up.players[7])
    else:
        p = sorted(match_up.players, key=lambda x: x['score'], reverse=True)
        matches = (p[0], p[1]), \
                  (p[2], p[3]), \
                  (p[4], p[5]), \
                  (p[6], p[7])
    return matches


def check_winner(player1: dict, player2: dict):
    print(f"{player1['name']}: Score = {player1['score']}\n "
          f"\t\tVS\n"
          f"{player2['name']}: Score = {player2['score']}")
    winner = [player1, player2, None]
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
            print(f"Please enter a valid response (must be 1, 2 or 3)")
            response = input(f"Choose a winner: ")
    return response
