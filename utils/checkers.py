import re
from datetime import date
from utils.constante import REGEX, GENDER, TIME_CONTROL
from models.player import pm


def check_name(value: str):
    check = input(f"{value.capitalize()}: ")
    while not re.match(REGEX, check):
        print(f'{value} invalide')
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


def check_players():
    players = []
    for i in range(1, 9):
        check = True
        identifier = input(f"Player {i} identifier: ")
        while check:
            try:
                if identifier not in players:
                    pm.find(identifier)
                    check = False
                else:
                    print(f'{identifier} already stored in database')
                    identifier = input(f"Player {i} identifier: ")
            except AttributeError:
                print(f'{identifier} not founded in database')
                identifier = input(f"Player {i} identifier: ")
        players.append(identifier)
    return players
