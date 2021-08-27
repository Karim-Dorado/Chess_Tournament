from typing import List, Tuple
from utils.view import View
from utils.constante import BIRTHDATE
from utils.checkers import check_name, check_gender, check_rank, check_date, check_time_control, check_description,\
    check_players


class Form(View):

    def __init__(self, title: str, choices: List[Tuple[str, str]]):
        content = '\n'.join([f'{choice}' for (choice, key) in choices])
        super().__init__(title, content)
        self.choices = choices

    def show(self):
        data = {}
        for (choice, key) in self.choices:
            if key in ["first_name", "last_name", "name", "place"]:
                data[key] = check_name(choice)
            elif key in ["birthdate"]:
                print("Birthdate")
                data[key] = check_date(BIRTHDATE)
            elif key in ["start_date", "end_date"]:
                if key == "start_date":
                    print("Start date")
                else:
                    print("End date")
                data[key] = check_date()
            elif key in ["gender"]:
                data[key] = check_gender()
            elif key in ["rank"]:
                data[key] = check_rank()
            elif key in ["time_control"]:
                data[key] = check_time_control()
            elif key in ["players"]:
                data[key] = check_players()
            elif key in ["description"]:
                data[key] = check_description()
        return data
